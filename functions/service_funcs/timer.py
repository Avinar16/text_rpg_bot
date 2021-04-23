def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    task = context.user_data['task_info']['task']
    duration = context.user_data['task_info']['duration']
    job_removed = remove_job_if_exists(
        str(chat_id),
        context
    )
    context.job_queue.run_once(
        task,
        duration,
        context=context,
        name=str(chat_id)
    )
    text = f'Эффект будет действовать {duration} секунд.'
    if job_removed:
        text += 'Действие предыдущего предмета развеялось. Будьте осторожны в следующий раз!'
    update.message.reply_text(text)


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True
