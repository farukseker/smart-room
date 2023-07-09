import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# İzlemek istediğiniz HTML template dosyalarının bulunduğu dizin
template_directory = "templates"

class TemplateChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Yalnızca dosya değişiklikleriyle ilgilenin
        if event.is_directory:
            return
        elif event.event_type == 'modified':
            # Uvicorn sunucusunu yeniden başlatın
            subprocess.run(["pkill", "-f", "uvicorn"])

# İzleyiciyi yapılandırın ve başlatın
event_handler = TemplateChangeHandler()
observer = Observer()
observer.schedule(event_handler, template_directory, recursive=True)
observer.start()

# Uygulamayı Uvicorn ile başlatın
subprocess.run(["uvicorn", "config.asgi:application", "--host", "192.168.0.111", "--port", "8000", "--reload"])
