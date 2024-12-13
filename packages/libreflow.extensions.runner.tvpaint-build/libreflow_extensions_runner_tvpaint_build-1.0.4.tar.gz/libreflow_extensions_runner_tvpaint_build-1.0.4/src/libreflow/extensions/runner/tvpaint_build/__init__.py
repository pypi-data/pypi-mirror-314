import os

from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.baseflow.file import GenericRunAction,TrackedFile,TrackedFolder,FileRevisionNameChoiceValue
from libreflow.baseflow.task import Task
from libreflow.utils.os import remove_folder_content

class CreateTvPaintFile(flow.Action):
    
    _task = flow.Parent()
    _shot = flow.Parent(3)
    _sequence = flow.Parent(5)
    _antc_path = flow.Computed(cached=True)

    def allow_context(self, context):
        return context

    def needs_dialog(self):
        self._antc_path.touch()
        self.message.set('<font color=orange>No animatic found</font>')
        return (self._antc_path.get() is None)
    
    def get_buttons(self):
        return ['Close']

    def start_tvpaint(self, path):
        start_action = self._task.start_tvpaint
        start_action.file_path.set(path)
        start_action.run(None)

    def execute_create_tvpaint_script(self, path, audio_path):
        exec_script = self._task.execute_create_tvpaint_script
        exec_script.ref_path.set(path)
        exec_script.audio_path.set(audio_path)
        exec_script.run(None)
    
    def _export_audio(self):
        file_oid = self._task.oid() + f'/files/{self._task.name()}_tvpp'
        print(file_oid)
        file = self.root().get_object(file_oid)
        export_audio = file.export_ae_audio
        ret = export_audio.run('Export')
        return ret

    def get_default_file(self, task_name, filename):
        file_mapped_name = filename.replace('.', '_')
        mng = self.root().project().get_task_manager()

        dft_task = mng.default_tasks[task_name]
        if not dft_task.files.has_mapped_name(file_mapped_name): # check default file
            # print(f'Scene Builder - default task {task_name} has no default file {filename} -> use default template')
            return None

        dft_file = dft_task.files[file_mapped_name]
        return dft_file

    def compute_child_value(self, child_value):
        if child_value is self._antc_path:
            self._antc_path.set(self.get_animatic_path())

    def get_animatic_path(self):
        if not self._shot.tasks.has_mapped_name('animatic'):
            return None
        task = self._shot.tasks['animatic']
        if not task.files.has_file('animatic', 'mov'):
            return None
        rev = task.files['animatic_mov'].get_head_revision()
        if (rev is None) \
            or (rev.get_sync_status() != 'Available'):
            return None
        path = rev.get_path()
        return path if os.path.isfile(path) else None

    def _ensure_file(self, name, format, path_format):

        files = self._task.files
        file_name = "%s_%s" % (name, format)

        if files.has_file(name, format):
            file = files[file_name]
        else:
            file = files.add_file(
                name=name,
                extension=format,
                tracked=True,
                default_path_format=path_format,
            )

        revision = file.create_working_copy()

        file.file_type.set('Works')

        return revision.get_path()

    def run(self,button):
        if button == 'Close':
            return
        
        self._export_audio()

        # path_format = None
        # task_name = self._task.name()
        # default_file = self.get_default_file(task_name, f"{task_name}.tvpp")
        # if default_file is not None:
        #     path_format = default_file.path_format.get()
        # anim_path = self._ensure_file(
        #     name=task_name,
        #     format="tvpp",
        #     path_format=path_format
        # )
        # self.start_tvpaint(anim_path)
        audio_path = self._antc_path.get().replace('.mov','.wav')
        self.execute_create_tvpaint_script(self._antc_path.get(),audio_path)


class StartTvPaint(GenericRunAction):

    file_path = flow.Param()

    def allow_context(self, context):
        return context

    def runner_name_and_tags(self):
        return 'TvPaint', []

    def target_file_extension(self):
        return 'tvpp'

    def extra_argv(self):
        return [self.file_path.get()]


class ExecuteCreateTvPaintScript(GenericRunAction):

    ref_path = flow.Param()
    audio_path = flow.Param()

    def allow_context(self, context):
        return context
    
    def runner_name_and_tags(self):
        return 'PythonRunner', []

    def get_version(self, button):
        return None

    def get_run_label(self):
        return "Create TvPaint Project"

    def extra_argv(self):
        current_dir = os.path.split(__file__)[0]
        script_path = os.path.normpath(os.path.join(current_dir,"scripts/project_template.py"))
        return [script_path, '--ref-path', self.ref_path.get(), '--audio-path', self.audio_path.get()]

class ReloadAudio(flow.Action):

    _task = flow.Parent()
    _shot = flow.Parent(3)

    def get_file(self):
        file_oid = self._task.oid() + f'/files/{self._task.name()}_tvpp'
        file = self.root().get_object(file_oid)
        return file

    def allow_context(self, context):
        # print(self._task.files.has_file(self._task.name(),'tvpp'))
        # print (self.get_file().is_empty())

        return self._task.files.has_file(self._task.name(),'tvpp') #and not self.get_file().is_empty()

    def needs_dialog(self):
        for sp in self.root().session().cmds.SubprocessManager.list_runner_infos():
                if sp['name'] == 'TvPaint' and sp['is_running'] and sp['label'] in ["Open file", 'TvPaint']:
                    if self.get_file().get_working_copy() is None :
                        user_name = self.root().project().get_user_name()
                        self.message.set(f'<font color=orange>No working copy found for this user ({user_name})</font>')
                        return True
                    return False
        
        self.message.set('<font color=orange>No running instance of TvPaint found</font>')
        return True
    
    def get_buttons(self):
        return ['Close']

    def execute_reload_audio_script(self, file_path, audio_path):
        exec_script = self._task.reload_audio_script
        exec_script.file_path.set(file_path)
        exec_script.audio_path.set(audio_path)
        exec_script.run(None)
    
    def _export_audio(self):
        export_audio = self.get_file().export_ae_audio
        ret = export_audio.run('Export')
        return ret
    
    def get_animatic_path(self):
        if not self._shot.tasks.has_mapped_name('animatic'):
            return None
        task = self._shot.tasks['animatic']
        if not task.files.has_file('animatic', 'mov'):
            return None
        rev = task.files['animatic_mov'].get_head_revision()
        if (rev is None) \
            or (rev.get_sync_status() != 'Available'):
            return None
        path = rev.get_path()
        return path if os.path.isfile(path) else None
    
    def run(self,button):
        if button == 'Close':
            return
        
        working_copy = self.get_file().get_working_copy()
        file_path = working_copy.get_path()
        audio_path = self._task.create_tv_paint_file._antc_path.get().replace('.mov','.wav')

        if not os.path.exists(audio_path) :
            self._export_audio()

        self.execute_reload_audio_script(file_path,audio_path)

class ReloadAudioScript(GenericRunAction):

    file_path = flow.Param()
    audio_path = flow.Param()

    def allow_context(self, context):
        return context
    
    def runner_name_and_tags(self):
        return 'PythonRunner', []

    def get_version(self, button):
        return None

    def get_run_label(self):
        return "Reload Audio"

    def extra_argv(self):
        current_dir = os.path.split(__file__)[0]
        script_path = os.path.normpath(os.path.join(current_dir,"scripts/reload_audio.py"))
        return [script_path,'--file-path', self.file_path.get(), '--audio-path', self.audio_path.get()]



def create_file(parent):
    if isinstance(parent, Task):
        r = flow.Child(CreateTvPaintFile)
        r.name = 'create_tv_paint_file'
        r.index = None
        return r

def start_tvpaint(parent):
    if isinstance(parent, Task):
        r = flow.Child(StartTvPaint)
        r.name = 'start_tvpaint'
        r.index = None
        r.ui(hidden=True)
        return r

def execute_create_tvpaint_script(parent):
    if isinstance(parent, Task):
        r = flow.Child(ExecuteCreateTvPaintScript)
        r.name = 'execute_create_tvpaint_script'
        r.index = None
        r.ui(hidden=True)
        return r

def reload_audio(parent):
    if isinstance(parent, Task):
        r = flow.Child(ReloadAudio)
        r.name = 'reload_audio'
        r.index = None
        return r

def reload_audio_script(parent):
    if isinstance(parent, Task):
        r = flow.Child(ReloadAudioScript)
        r.name = 'reload_audio_script'
        r.index = None
        r.ui(hidden=True)
        return r


def install_extensions(session):
    return {
        "tvpaint_build": [
            create_file,
            start_tvpaint,
            execute_create_tvpaint_script,
            reload_audio,
            reload_audio_script,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
