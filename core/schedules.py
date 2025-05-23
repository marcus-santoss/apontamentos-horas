import random
from datetime import timedelta


def get_value(prop):
    return random.randint(prop.min, prop.max)


def get_timedelta_value(prop):
    return timedelta(minutes=get_value(prop))


def get_lunch_end_time(current_time):
    from core.utils import get_configs
    configs = get_configs()
    if configs.periods.lunch_start <= current_time < configs.periods.lunch_end:
        current_time = configs.periods.lunch_end + get_timedelta_value(
            configs.lunch_variation
        )
    return current_time


def generate_schedule_with_descriptions(tasks: list):
    from core.utils import get_configs
    configs = get_configs()

    annotations = []
    common_tasks = tasks[:]  # Faz uma cópia para evitar alterações
    task_num = get_value(configs.task_per_day)
    remaining_minutes = get_value(configs.minutes_per_day)
    current_time = configs.periods.start_time + get_timedelta_value(
        configs.start_time_variation
    )
    task_avg_minutes = remaining_minutes // task_num

    while remaining_minutes > 0:
        description = random.choice(common_tasks)
        common_tasks.remove(description)

        # Configurar a hora do almoço
        current_time = get_lunch_end_time(current_time)

        # Limitar a duração a 3 horas (180 minutos)
        duration_minutes = min(
            configs.max_task_duration, task_avg_minutes, remaining_minutes
        )

        pause = get_value(configs.pause)
        task_duration = timedelta(minutes=duration_minutes + pause)
        task_end_time = current_time + task_duration

        if task_end_time > configs.periods.end_time:
            task_end_time = configs.periods.end_time
            task_duration = task_end_time - current_time
            duration_minutes = int(task_duration.total_seconds() / 60)

        # Não atribui tasks de estudo e tempo disponivel depois do horário comercial
        if "Tempo" in description and (
                current_time >= configs.periods.comercial_end
                or task_end_time >= configs.periods.comercial_end
        ):
            continue

        annotations.append(
            {
                "description": description,
                "start": current_time.strftime("%H:%M"),
                "end": task_end_time.strftime("%H:%M"),
                "duration": str(task_duration),
            }
        )

        task_variation = get_value(configs.task_variation)
        current_time = task_end_time + timedelta(minutes=task_variation)
        remaining_minutes -= duration_minutes + pause

        if current_time >= configs.periods.end_time or remaining_minutes <= 0:
            break

    return annotations
