def linear(interval=1, offset=0):
    docstring = "Track at iterations {" + f"{offset} + n * {interval} " + "| n >= 0}."

    def schedule(global_step):
        shifted = global_step - offset
        return shifted >= 0 and shifted % interval == 0

    schedule.__doc__ = docstring

    return schedule


schedulers = {
    'linear': linear
}


class ScheduleSelector:
   
    @staticmethod
    def select(schedule_name):
        if len(schedule_name) == 0:
            return linear()
        schedule, augs = ScheduleSelector.parse_schedule(schedule_name)
        if schedule not in schedulers:
            raise NotImplementedError(f"hook not found: {schedule}")
        return schedulers[schedule](*augs)
    
    @staticmethod
    def parse_schedule(schedules):
        schedule = schedules[:schedules.index("(")].strip()
        schedule_argument = schedules[schedules.index("(")+1: -1].strip()
        augs = [int(x.strip()) for x in schedule_argument.split(',')]
        return schedule, augs

