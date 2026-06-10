import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
SENDGRID_ENABLED = bool(SENDGRID_API_KEY and EMAIL_FROM)


def _send_email(to_email: str, subject: str, body: str) -> None:
    if SENDGRID_ENABLED:
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            message = Mail(
                from_email=EMAIL_FROM,
                to_emails=to_email,
                subject=subject,
                html_content=body,
            )
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            logger.info(f"[MAIL] Email enviado para {to_email} | Status: {response.status_code}")
        except Exception as e:
            logger.error(f"[MAIL] Falha ao enviar email para {to_email}: {e}")
    else:
        logger.info(
            f"\n"
            f"============================================================\n"
            f"[NOTIFICACAO] {subject}\n"
            f"  Para : {to_email}\n"
            f"============================================================"
        )


def notify_task_created(user_name: str, user_email: str, task_title: str, category: str) -> None:
    subject = f"Nova tarefa atribuida: {task_title}"
    body = (
        f"<p>Ola, <strong>{user_name}</strong>!</p>"
        f"<p>Uma nova tarefa foi atribuida a voce:</p>"
        f"<ul>"
        f"<li><strong>Titulo:</strong> {task_title}</li>"
        f"<li><strong>Categoria:</strong> {category or 'N/A'}</li>"
        f"<li><strong>Status:</strong> A fazer</li>"
        f"</ul>"
    )
    _send_email(user_email, subject, body)


def notify_task_updated(user_name: str, user_email: str, task_title: str, old_status: str, new_status: str, reassigned: bool = False) -> None:
    if reassigned:
        subject = f"Tarefa atribuida a voce: {task_title}"
        body = (
            f"<p>Ola, <strong>{user_name}</strong>!</p>"
            f"<p>Uma tarefa foi reatribuida a voce:</p>"
            f"<ul>"
            f"<li><strong>Titulo:</strong> {task_title}</li>"
            f"<li><strong>Status:</strong> {new_status}</li>"
            f"</ul>"
        )
    else:
        subject = f"Tarefa atualizada: {task_title}"
        body = (
            f"<p>Ola, <strong>{user_name}</strong>!</p>"
            f"<p>Uma das suas tarefas foi atualizada:</p>"
            f"<ul>"
            f"<li><strong>Titulo:</strong> {task_title}</li>"
            f"<li><strong>Status anterior:</strong> {old_status}</li>"
            f"<li><strong>Novo status:</strong> {new_status}</li>"
            f"</ul>"
        )
    _send_email(user_email, subject, body)


def notify_task_deleted(user_name: str, user_email: str, task_title: str) -> None:
    subject = f"Tarefa removida: {task_title}"
    body = (
        f"<p>Ola, <strong>{user_name}</strong>!</p>"
        f"<p>A seguinte tarefa foi removida do sistema:</p>"
        f"<ul>"
        f"<li><strong>Titulo:</strong> {task_title}</li>"
        f"</ul>"
    )
    _send_email(user_email, subject, body)