from django.db.models import Exists, OuterRef, Q
from wbcore import filters as wb_filters
from wbcore.contrib.directory.models import Entry, Person
from wbcore.filters.defaults import year_to_date_range
from wbcore.pandas.filterset import PandasFilterSetMixin
from wbcore.utils.date import current_financial_quarter
from wbcrm.models.accounts import Account, AccountRole
from wbfdm.models import Classification, ClassificationGroup
from wbfdm.preferences import get_default_classification_group
from wbportfolio.models import Product, ProductGroup
from wbportfolio.models.transactions.claim import Claim, ClaimGroupbyChoice
from wbportfolio.preferences import get_monthly_nnm_target


class CustomerAPIFilter(wb_filters.FilterSet):
    external_id = wb_filters.CharFilter(label="External ID", lookup_expr="exact")

    class Meta:
        model = Claim
        fields = []


class CustomerClaimFilter(wb_filters.FilterSet):
    class Meta:
        model = Claim
        fields = {"date": ["gte", "lte", "exact"], "status": ["exact"], "product": ["exact"], "bank": ["exact"]}


def get_entry_queryset(request):
    """
    Show only entry which have a account role the user can see
    """
    roles = AccountRole.objects.filter_for_user(request.user)
    return Entry.objects.filter(account_roles__in=roles)


class CommissionBaseFilterSet(wb_filters.FilterSet):
    account_owner = wb_filters.ModelMultipleChoiceFilter(
        label="Account Owner",
        queryset=Entry.objects.all(),
        endpoint=Entry.get_representation_endpoint(),
        value_key=Entry.get_representation_value_key(),
        label_key=Entry.get_representation_label_key(),
        filter_params={"with_account": True},
        method="filter_account_owner",
    )

    not_account_owner = wb_filters.ModelMultipleChoiceFilter(
        column_field_name="account_owner",
        lookup_icon="!=",
        lookup_label="Not Equals",
        queryset=Entry.objects.all(),
        endpoint=Entry.get_representation_endpoint(),
        value_key=Entry.get_representation_value_key(),
        label_key=Entry.get_representation_label_key(),
        filter_params={"with_account": True},
        method="filter_not_owner",
    )

    product = wb_filters.ModelMultipleChoiceFilter(
        label="Product",
        method="filter_product",
        queryset=Product.objects.all(),
        endpoint=Product.get_representation_endpoint(),
        value_key=Product.get_representation_value_key(),
        label_key=Product.get_representation_label_key(),
    )
    product_group = wb_filters.ModelChoiceFilter(
        label="Product Group",
        method="filter_productgroup",
        queryset=ProductGroup.objects.all(),
        endpoint=ProductGroup.get_representation_endpoint(),
        value_key=ProductGroup.get_representation_value_key(),
        label_key=ProductGroup.get_representation_label_key(),
    )

    account = wb_filters.ModelChoiceFilter(
        label="Account",
        method="filter_account",
        queryset=Account.objects.all(),
        endpoint=Account.get_representation_endpoint(),
        value_key=Account.get_representation_value_key(),
        label_key=Account.get_representation_label_key(),
        filter_params={"status": "OPEN"},
    )

    manager_role = wb_filters.ModelChoiceFilter(
        label="Manager Role",
        queryset=get_entry_queryset,
        endpoint=Entry.get_representation_endpoint(),
        value_key=Entry.get_representation_value_key(),
        label_key=Entry.get_representation_label_key(),
        filter_params={"with_account_role": True},
        method="filter_manager_role",
    )

    classification = wb_filters.ModelChoiceFilter(
        label="Classification",
        queryset=Classification.objects.all(),
        endpoint=Classification.get_representation_endpoint(),
        value_key=Classification.get_representation_value_key(),
        label_key=Classification.get_representation_label_key(),
        filter_params={"instrument_type_key": "product"},
        method="filter_classification",
    )

    def filter_account(self, queryset, name, value):
        if value:
            return queryset.filter(account__in=value.get_descendants(include_self=True).values("id"))
        return queryset

    def filter_product(self, queryset, name, value):
        if value:
            return queryset.filter(product__in=value)
        return queryset

    def filter_productgroup(self, queryset, name, value):
        if value:
            return queryset.filter(product__parent=value)
        return queryset

    def filter_account_owner(self, queryset, name, value):
        if value:
            return queryset.filter(account__in=Account.get_accounts_for_customer(value))
        return queryset

    def filter_not_owner(self, queryset, name, value):
        if value:
            return queryset.exclude(account__in=Account.get_accounts_for_customer(value))
        return queryset

    def filter_manager_role(self, queryset, name, value):
        if value:
            return queryset.filter(account__in=Account.get_managed_accounts_for_entry(value).values("id"))
        return queryset

    def filter_classification(self, queryset, name, value):
        if value:
            return queryset.filter(product__classifications=value)
        return queryset


class ClaimFilter(CommissionBaseFilterSet):
    pending_approval = wb_filters.BooleanFilter(label="Pending Approval", method="boolean_pending_approval")
    linked_trade = wb_filters.BooleanFilter(method="filter_trade_isnotnull", label="Trade Linked")
    in_charge_of_customer = wb_filters.ModelChoiceFilter(
        label="In Charge of Customer",
        method="filter_in_charge_of_customer",
        queryset=Person.objects.all(),
        endpoint=Person.get_representation_endpoint(),
        value_key=Person.get_representation_value_key(),
        label_key=Person.get_representation_label_key(),
    )

    def filter_in_charge_of_customer(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(claimant__relationship_managers=value)
                | Q(root_account__customers__entry__relationship_managers=value)  # TODO optimize this
            ).distinct("id")
        return queryset

    def filter_trade_isnotnull(self, queryset, name, value):
        if value is True:
            return queryset.filter(trade__isnull=False)
        elif value is False:
            return queryset.filter(trade__isnull=True)
        return queryset

    def boolean_pending_approval(self, queryset, name, value):
        if value is True:
            return queryset.filter(status=Claim.Status.PENDING, account__isnull=False, trade__isnull=False)
        elif value is False:
            return queryset.filter(status__in=[Claim.Status.APPROVED])
        return queryset

    class Meta:
        model = Claim
        fields = {
            "date": ["gte", "lte", "exact"],
            "status": ["exact"],
            # "trade": ["exact"],
            "bank": ["exact", "icontains"],
            "claimant": ["exact"],
            "shares": ["gte", "lte", "exact"],
            "reference": ["exact", "icontains"],
            "creator": ["exact"],
        }


class ClaimGroupByFilter(ClaimFilter):
    pending_approval = in_charge_of_customer = linked_trade = None

    only_new_customer = wb_filters.BooleanFilter(method="filter_only_new_customer", label="Only new customers")

    group_by = wb_filters.ChoiceFilter(
        label="Group By",
        choices=ClaimGroupbyChoice.choices(),
        default=ClaimGroupbyChoice.PRODUCT.name,
        method=lambda queryset, label, value: queryset,
        required=True,
        clearable=False,
    )

    date = wb_filters.DateRangeFilter(
        label="Date Range",
        method=lambda queryset, label, value: queryset,
        required=True,
        clearable=False,
        default=year_to_date_range,
    )

    groupby_classification_group = wb_filters.ModelChoiceFilter(
        default=lambda k, v, f: get_default_classification_group().id,
        method=lambda queryset, label, value: queryset,
        label="Group by Classification Group",
        queryset=ClassificationGroup.objects.all(),
        endpoint=ClassificationGroup.get_representation_endpoint(),
        value_key=ClassificationGroup.get_representation_value_key(),
        label_key=ClassificationGroup.get_representation_label_key(),
        depends_on=[{"field": "group_by", "options": {"activates_on": [ClaimGroupbyChoice.CLASSIFICATION.name]}}],
    )

    def filter_only_new_customer(self, queryset, name, value):
        if value:
            past_accounts = Account.all_objects.annotate(
                has_past_claims=Exists(
                    queryset.filter(date__lt=self.view.start_date, account__tree_id=OuterRef("tree_id"))
                )
            ).filter(has_past_claims=True)
            return queryset.exclude(account__in=past_accounts)
        return queryset

    class Meta:
        model = Claim
        fields = {}


class ConsolidatedTradeSummaryTableFilterSet(PandasFilterSetMixin, ClaimGroupByFilter):
    class Meta:
        model = Claim
        fields = {}
        df_fields = {
            "sum_shares_start__lte": wb_filters.NumberFilter(
                label="Sum Shares Start", lookup_expr="gte", field_name="sum_shares_start"
            ),
            "sum_shares_start__gte": wb_filters.NumberFilter(
                label="Sum Shares Start", lookup_expr="lte", field_name="sum_shares_start"
            ),
            "sum_shares_end__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Sum Shares End", field_name="sum_shares_end"
            ),
            "sum_shares_diff__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Difference Shares", field_name="sum_shares_diff"
            ),
            "sum_aum_start__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Sum AUM Start", field_name="sum_aum_start"
            ),
            "sum_aum_end__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Sum AUM End", field_name="sum_aum_end"
            ),
            "sum_aum_diff__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Nominal difference", field_name="sum_aum_diff"
            ),
            "sum_aum_perf__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Pourcent difference", field_name="sum_aum_perf"
            ),
            "sum_shares_end__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Sum Shares End", field_name="sum_shares_end"
            ),
            "sum_shares_diff__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Difference Shares", field_name="sum_shares_diff"
            ),
            "sum_aum_start__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Sum AUM Start", field_name="sum_aum_start"
            ),
            "sum_aum_end__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Sum AUM End", field_name="sum_aum_end"
            ),
            "sum_aum_diff__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Nominal difference", field_name="sum_aum_diff"
            ),
            "sum_aum_perf__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Pourcent difference", field_name="sum_aum_perf"
            ),
        }


class CumulativeNNMChartFilter(ClaimGroupByFilter):
    groupby_classification_group = group_by = None

    hide_projected_monthly_nnm_target = wb_filters.BooleanFilter(
        default=True, label="Hide Target line", method=lambda queryset, label, value: queryset
    )
    projected_monthly_nnm_target = wb_filters.NumberFilter(
        default=lambda k, v, f: get_monthly_nnm_target(),
        method=lambda queryset, label, value: queryset,
        label="Projected Monthly NNM Target",
    )

    class Meta:
        model = Claim
        fields = {}


class ProfitAndLossPandasFilter(PandasFilterSetMixin, ClaimFilter):
    pending_approval = None

    recipient = wb_filters.ModelChoiceFilter(
        label="Recipient",
        queryset=Entry.objects.all(),
        endpoint=Entry.get_representation_endpoint(),
        value_key=Entry.get_representation_value_key(),
        label_key=Entry.get_representation_label_key(),
        filter_params={"with_account": True},
        method="filter_recipient",
    )

    date = wb_filters.FinancialPerformanceDateRangeFilter(
        label="Date Range",
        method=lambda queryset, label, value: queryset,
        required=True,
        clearable=False,
        default=current_financial_quarter,
    )

    class Meta:
        model = Claim
        fields = {"product": ["exact"], "account": ["exact"]}
        df_fields = {
            "unrealized_pnl__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Unrealized P&L", field_name="unrealized_pnl"
            ),
            "realized_pnl__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Realized P&L", field_name="realized_pnl"
            ),
            "total_pnl__lte": wb_filters.NumberFilter(lookup_expr="lte", label="Total P&L", field_name="total_pnl"),
            "total_invested__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Total Invested", field_name="total_invested"
            ),
            "performance__lte": wb_filters.NumberFilter(
                lookup_expr="lte", label="Performance", field_name="performance"
            ),
            "unrealized_pnl__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Unrealized P&L", field_name="unrealized_pnl"
            ),
            "realized_pnl__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Realized P&L", field_name="realized_pnl"
            ),
            "total_pnl__gte": wb_filters.NumberFilter(lookup_expr="gte", label="Total P&L", field_name="total_pnl"),
            "total_invested__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Total Invested", field_name="total_invested"
            ),
            "performance__gte": wb_filters.NumberFilter(
                lookup_expr="gte", label="Performance", field_name="performance"
            ),
        }


class CustomerClaimGroupByFilter(ClaimGroupByFilter):
    product = wb_filters.ModelChoiceFilter(
        label="Product",
        queryset=Product.objects.all(),
        endpoint=Product.get_representation_endpoint(),
        value_key=Product.get_representation_value_key(),
        label_key="{{title}} {{currency_repr}} - {{isin}} - {{bank_repr}}",
    )

    class Meta:
        model = Claim
        fields = {
            "account": ["exact"],
        }


class NegativeTermimalAccountPerProductFilterSet(wb_filters.FilterSet):
    sum_shares__gte = wb_filters.NumberFilter(lookup_expr="gte", field_name="sum_shares", label="Total Shares")
    sum_shares__lte = wb_filters.NumberFilter(lookup_expr="lte", field_name="sum_shares", label="Total Shares")

    only_approved = wb_filters.BooleanFilter(
        default=False, label="Only Approved claims", method="filter_only_approve_claims"
    )

    def filter_only_approve_claims(self, queryset, name, value):
        if value is True:
            return queryset.filter(status=Claim.Status.APPROVED)
        return queryset

    class Meta:
        model = Claim
        fields = {
            "product": ["exact"],
            "account": ["exact"],
        }
