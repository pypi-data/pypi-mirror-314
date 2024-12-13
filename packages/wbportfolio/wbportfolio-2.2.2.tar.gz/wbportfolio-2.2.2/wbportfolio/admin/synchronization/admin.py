from django_celery_beat.admin import (
    PeriodicTaskAdmin,
    PeriodicTaskForm,
    _,
    loads,
    messages,
    pluralize,
)


class SynchronizationTaskForm(PeriodicTaskForm):
    def clean(self):
        return self.cleaned_data


class SynchronizationAdmin(PeriodicTaskAdmin):
    form = SynchronizationTaskForm
    search_fields = ("name",)
    regtask = None
    readonly_fields = (
        "last_run_at",
        # 'regtask',
        "task",
        "args",
        # 'kwargs',
        "expires",
        "expire_seconds",
        "queue",
        "exchange",
        "routing_key",
        "priority",
        "headers",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "task",
                    "enabled",
                    "description",
                ),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Schedule",
            {
                "fields": ("crontab", "start_time", "last_run_at", "one_off"),
                "classes": ("extrapretty", "wide"),
            },
        ),
        (
            "Arguments",
            {
                "fields": ("args", "kwargs"),
                "classes": ("extrapretty", "wide", "collapse", "in"),
            },
        ),
        (
            "Execution Options",
            {
                "fields": ("expires", "expire_seconds", "queue", "exchange", "routing_key", "priority", "headers"),
                "classes": ("extrapretty", "wide", "collapse", "in"),
            },
        ),
    )

    def run_tasks(self, request, queryset):
        def _load_kwargs(task):
            kwargs = loads(task.kwargs)
            kwargs["override_execution_datetime_validity"] = True
            return kwargs

        self.celery_app.loader.import_default_modules()

        tasks = [
            (self.celery_app.tasks.get(task.task), loads(task.args), _load_kwargs(task), task.queue)
            for task in queryset
        ]

        if any(t[0] is None for t in tasks):
            for i, t in enumerate(tasks):
                if t[0] is None:
                    break

            # variable "i" will be set because list "tasks" is not empty
            not_found_task_name = queryset[i].task

            self.message_user(
                request,
                _('task "{0}" not found'.format(not_found_task_name)),
                level=messages.ERROR,
            )
            return

        task_ids = [
            task.apply_async(args=args, kwargs=kwargs, queue=queue)
            if queue and len(queue)
            else task.apply_async(args=args, kwargs=kwargs)
            for task, args, kwargs, queue in tasks
        ]
        tasks_run = len(task_ids)
        self.message_user(
            request,
            _("{0} task{1} {2} successfully run").format(
                tasks_run,
                pluralize(tasks_run),
                pluralize(tasks_run, _("was,were")),
            ),
        )

    run_tasks.short_description = _("Run selected tasks")
