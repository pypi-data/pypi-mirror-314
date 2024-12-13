# import multiprocessing
# from time import sleep
# import os
# import logging
# from scp import SCPClient
# import paramiko

# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler, LoggingEventHandler

# class EventHandler(FileSystemEventHandler):
#     def __init__(self, ip):
#         super().__init__()
         
#         self.ssh = paramiko.SSHClient()
#         # self.ssh.load_system_host_keys()
#         self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         self.ssh.connect(ip, username='ubuntu', key_filename=os.path.expanduser("~/.thunder/id_rsa"))        

#         self.sftp = self.ssh.open_sftp()
#         self.scp = SCPClient(self.ssh.get_transport())
#         self.cwd = os.path.dirname(os.getcwd())
        
#     def on_created(self, event):
#         try:
#             # logger.info(f"CREATE {event}")
#             if not event.is_directory:
#                 self._sync_file(event.src_path)
#         except Exception as e:
#             return
        
#     def on_deleted(self, event):
#         try:
#             # logger.info(f"DELETE {event}")
#             if not event.is_directory:
#                 self._delete_file(event.src_path)
#         except Exception as e:
#             return

#     def on_modified(self, event):
#         try:
#             # logger.info(f"MODIFIED {event}")
#             if not event.is_directory:
#                 self._sync_file(event.src_path)
#         except Exception as e:
#             return
        
#     def on_moved(self, event):
#         try:
#             # logger.info(f"MOVED {event}")
#             if not event.is_directory:
#                 self._delete_file(event.src_path)
#                 # logger.info("syncing")
#                 self._sync_file(event.dest_path)
#                 # logger.info("synced")
#         except Exception as e:
#             # logger.info(f"failed to do something {e}")
#             return
        
#     def _sync_file(self, filepath):
#         self.scp.put(filepath, self._get_remote_path(filepath))
        
#     def _delete_file(self, filepath):
#         try:
#             # logger.info(f"deleting file {self._get_remote_path(filepath)}")
#             self.sftp.remove(self._get_remote_path(filepath))
#         except FileNotFoundError as e:
#             # logger.info(f"some delete error {e}")
#             return
    
#     def _get_remote_path(self, local_path):
#         return local_path[len(self.cwd):].strip()[1:]

# def start_file_sync(is_done_event, ip):
#     # Setup observer
#     event_handler = EventHandler(ip)
#     observer = Observer()
#     observer.schedule(event_handler, os.getcwd(), recursive=True)
#     observer.start()

#     # Main loop
#     parent = multiprocessing.parent_process()
#     while parent.is_alive() and not is_done_event.is_set():
#         sleep(1)
        
#     observer.stop()
#     observer.join()
    