# coding: utf-8
#/*##########################################################################
# Copyright (C) 2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/

"""
This module is used to manage rsync commands.
"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "04/05/2020"

from .utils import Borg
import subprocess
import functools
import shutil
import sys
import os
# TODO: remove dependency on qt
from silx.gui import qt
from queue import Queue
import logging

logger = logging.getLogger(__name__)


# simple structure to merge several callback and launch a new one when all
# received
class _MergeCallback(qt.QObject):
    def __init__(self, n_call, callback, callback_parameters):
        super().__init__()
        self.needed_callback = n_call
        self._n_callback = 0
        self.callback = callback
        self.callback_parameters = callback_parameters

    def call(self):
        self._n_callback += 1
        if self._n_callback >= self.needed_callback:
            if self.callback_parameters is not None:
                self.callback(*self.callback_parameters)
            else:
                self.callback()


def singleton(class_):
    instances = {}
    def wrapper(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return wrapper


@singleton
class RSyncManager(qt.QObject):
    """The manager is managing stacks to call the `rsync` command of the
    system.
    This is used to make interface and make sure only command to rsync is
    called for a tuple of (source folder, target folder) and avoid overhead.
    """

    def __init__(self):
        qt.QObject.__init__(self)
        self.rsyncQueues = {}
        """link couple of (source, target) to a Queue of thread. Because rsync
        action can't be runned in concurence."""
        self.rmfiles = {}
        self._force_sync = False

    @property
    def force_sync(self):
        return self._force_sync

    @force_sync.setter
    def force_sync(self, force):
        """
        will wait every time to the worker until the operation is not done
        """
        if force is True:
            logger.info('RSyncManager synchronisation forced')
        else:
            logger.info('RSyncManager synchronisation release')

        self._force_sync = force

    def sync_files(self, sources, targets, wait=False, delete=None,
                   callback=None, callback_parameters=None, parallel=False,
                   verbose=False, rights=None):
        """sync a list of file

        :param tuple source: set of file to synchronize.
        :param tuple target: destination of each source.
        :param bool wait: Standard behavior is to create a thread dealing with
                           rsync hen release RSyncManager. If block is True
                           then RSync will wait until the thread is processed.
        :param tuple delete: if True, will delete the source folder after sync
        :param callback: function to launch once the thread is terminated
        :param callback_parameters: parameters to give to hte callback
        :param bool parallel: True if we want to launch rsync in parallel mode.
        :param bool verbose: True if we want to call Rsync in verbose mode
        :param Union[None, int] rights: if we want to change rights on target
                                        files should be set to a valid rights
                                        id (777, 621...)
        """
        if not len(sources) == len(targets):
            raise ValueError('you should provide one target per source')

        if callback is not None:
            callback_obj = _MergeCallback(n_call=len(sources),
                                          callback=callback,
                                          callback_parameters=callback_parameters)
        else:
            callback_obj = None

        for source, target, _delete in zip(sources, targets, delete):
            if callback_obj is not None:
                self.sync_file(source=source, target=target, wait=wait,
                               delete=_delete, callback=callback_obj.call,
                               callback_parameters=None, parallel=parallel,
                               verbose=verbose, rights=rights)
            else:
                self.sync_file(source=source, target=target, wait=wait,
                               delete=_delete, callback=None,
                               callback_parameters=None, parallel=parallel,
                               verbose=verbose, rights=rights)

    def sync_file(self, source, target, wait=False, delete=False,
                  callback=None, callback_parameters=None, parallel=False,
                  verbose=False, rights=None):
        """sync a file

        :param str source: the path of the folder or path to sync. If is a
                           folder will synchronize recursively
        :param str target:
        :param bool wait: Standard behavior is to create a thread dealing with
                           rsync hen release RSyncManager. If block is True
                           then RSync will wait until the thread is processed.
        :param bool delete: if True, will delete the source folder after sync
        :param callback: function to launch once the thread is terminated
        :param callback_parameters: parameters to give to hte callback
        :param bool parallel: True if we want to launch rsync in parallel mode.
        :param bool verbose: True if we want to call Rsync in verbose mode
        :param Union[None, int] rights: if we want to change rights on target
                                        files should be set to a valid rights
                                        id (777, 621...)
        """
        options = ['--times']
        if os.path.isdir(source):
            options.append('--recursive')

        if delete is True:
            options.append('--remove-source-files')
        else:
            options.append('--update')

        if verbose is True:
            options.append('--verbose')

        if rights is not None:
            options.append('--perms --chmod={}'.format(rights))

        return self.sync_folder_raw(source=source,
                                    target=target,
                                    options=options,
                                    block=wait,
                                    callback=callback,
                                    callback_parameters=callback_parameters,
                                    parallel=parallel)

    def _get_queue(self, key, finish_handler):
        if key not in self.rsyncQueues:
            rsyncQueue = _RSyncQueue()
            rsyncQueue.sigQueueFinished.connect(finish_handler)
            self.rsyncQueues[key] = rsyncQueue
        return self.rsyncQueues[key]

    def has_active_sync(self, source, target, timeout=6)-> bool:
        """
        Check if a synchronization between source and target exists

        :param str source:
        :param str target:
        :return:
        :rtype: bool
        """
        command = ' '.join(['ps -aux', '| grep rsync', '|grep ' + source,
                            '|grep ' + target, '| wc -l'])
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as process:
            try:
                stdout, stderr = process.communicate(input=None,
                                                     timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                logger.error('timeout exceeded')
                raise subprocess.TimeoutExpired(process.args, timeout,
                                                output=stdout,
                                                stderr=stderr)
            except:  # Including KeyboardInterrupt, communicate handled that.
                process.kill()
                # We don't call process.wait() as .__exit__ does that for us.
                raise
            else:
                try:
                    out = stdout.decode('utf-8')
                except:
                    logger.error('Fail to decode stdout')
                    return False
                else:
                    try:
                        n_rsync = int(out) - 1
                    except Exception as e:
                        logger.error('fail to convert (return of the command '
                                     'should be an int)', str(e))
                        return False
                    else:
                        return n_rsync > 1

    def remove_sync_files(self, dir, files, block=False):
        """
        Remove some files from a specific forlder but taking into account the
        fact some files could have been synchronized or under synchronization.

        :param dir: origin of the directory
        :param files: files to remove
        :param bool block: Standard behavior is to create a thread dealing with
        """
        _filesToRemove = set(files)
        # take into account ongoing sync
        if dir in self.rsyncQueues:
            for f in files:
                _filesToRemove.add(f.replace(dir, self.rsyncQueues[dir]))

        _queue = self._get_queue((dir, None), self._managed_finished_rm)
        _queue.add_action(action='rm',
                          source=dir,
                          files=_filesToRemove)
        if block is True or self._force_sync is True:
            self.rsyncQueues[(dir, None)].rsyncThread.wait()

    def sync_folder_raw(self, source, target, options, block=False,
                        callback=None, callback_parameters=None, parallel=False,
                        timeout=5):
        """sync a folder launching directly the options given. Used for
        benchmarking.

        :param str source: the path of the folder to sync
        :param str target:
        :param bool block: Standard behavior is to create a thread dealing with
            rsync hen release RSyncManager. If block is True then RSync will
            wait until the thread is processed.
        :param list options: the list of options to apply
        :param handler: function to launch once the thread is terminated
        :param bool parallel: True if we want to launch rsync in parallel mode.
        """
        target = target.rstrip(os.path.sep)
        if os.path.isdir(source):
            targ_dir = target
        else:
            targ_dir = os.path.dirname(target)
        if not os.path.isdir(targ_dir):
            try:
                os.makedirs(targ_dir)
            except Exception as e:
                err = 'Unable to create target dir {}. Error is {}'.format(targ_dir, str(e))
                logger.error(err)
                return
        if block is True or self._force_sync is True:
            # wait until al thread are ended
            while (source, target) in self.rsyncQueues:
                self.rsyncQueues[(source, target)].wait(timeout)

        _queue = self._get_queue((source, target), self._managed_finished_sync)
        _queue.add(source=source, target=target, options=options,
                   parallel=parallel, callback=callback,
                   callback_parameters=callback_parameters)

        if block is True or self._force_sync is True:
            self.rsyncQueues[(source, target)].rsyncThread.wait(timeout)

    def _managed_finished_sync(self, source, target):
        if self.rsyncQueues[(source, target)].empty() is True:
            self.rsyncQueues[(source, target)].sigQueueFinished.disconnect(
                self._managed_finished_sync)
            del self.rsyncQueues[(source, target)]

    def _managed_finished_rm(self, source):
        if self.rsyncQueues[(source, None)].empty() is True:
            self.rsyncQueues[(source, None)].sigQueueFinished.disconnect(
                self._managed_finished_rm)
            del self.rsyncQueues[(source, None)]

    @staticmethod
    def has_rsync():
        if not sys.platform.startswith('linux'):
            return False
        try:
            subprocess.call(["rsync", "--version"], stdout=subprocess.PIPE)
        except OSError:
            return False
        else:
            return True

    @staticmethod
    def get_rsync_command(source, target, options, parallel):
        command = ""
        if parallel is True and RSyncManager().canUseParallel():
            command += "parallel -j8 "
        command = "rsync"
        for option in options:
            command += " " + option
        command += " " + source
        command += " " + target
        return command

    @staticmethod
    def can_use_parallel():
        """True if we can use rsync in parallel mode"""
        try:
            subprocess.call(["parallel", "--version"], stdout=subprocess.PIPE)
        except OSError:
            return False
        else:
            return True

    def sync_file_raw(self, src, dst):
        """synchronize the two files inplace.
        warning: won't create any stack for it"""
        try:
            subprocess.call(["rsync", src, dst, '--inplace'])
        except OSError as e:
            logger.error('fail to symchronize files', src, dst, '. Reason is', e)


class SetQueue(Queue):
    """Queue with a set behavior. In the sense that a requested thread
    synchronization could not be present twice"""
    def __init__(self, maxsize=0):
        Queue.__init__(self, maxsize)
        self._existing = []

    def put(self, val):
        thread, callbacks = val
        _id = self._get_id(thread)
        if _id in self._existing:
            return
        else:
            self._existing.append(_id)
            Queue.put(self, val)

    def get(self):
        thread, callbacks = Queue.get(self)
        _id = self._get_id(thread)
        if _id in self._existing:
            self._existing.remove(_id)
        return thread, callbacks

    def _get_id(self, thread):
        """
        Get hash from thread source, target and options / files to make sure
        actions are uniques and won't be stored several time
        """
        if isinstance(thread, _RmThread):
            return (thread.source, None, thread.files_to_rm)
        elif isinstance(thread, _RSyncThread):
            return (thread._source, thread._target, thread._options)
        else:
            raise ValueError('Unrecognized thread type')


class _RSyncQueue(SetQueue, qt.QObject):
    """
    class to deal with the RSync thread and avoid competition of rsync commands
    """

    sigQueueFinished = qt.Signal(str, str)

    def __init__(self):
        SetQueue.__init__(self)
        qt.QObject.__init__(self)
        self.rsyncThread = None
        self.callback = None
        self.callback_parameters = None
        self.threads = []

    def add(self, source, target, options, parallel, callback, callback_parameters):
        thread = _RSyncThread(source=source,
                              target=target,
                              options=options,
                              parallel=parallel)
        self.threads.append(thread)
        callback_finisher = functools.partial(self.sync_finisher, source, target)
        if callback is not None:
            if callback_parameters is None:
                callback_parameters = tuple()
            handler_callback = functools.partial(callback, *callback_parameters)
            self.put((thread, (callback_finisher, handler_callback)))
        else:
            self.put((thread, (callback_finisher, )))
        if self.can_exec_next():
            self.exec_next()

    def add_action(self, source, action, files=None):
        assert action in ('rm', 'rmdir')
        if action == 'rm':
            thread = _RmThread(source=source, files_to_rm=files)
            callback = functools.partial(self.sync_finisher, source, None)
        else:
            thread = _RmThread(source=source, files_to_rm=(source,))
            callback = functools.partial(self.sync_finisher, source, None)

        self.put((thread, (callback, )))
        if self.can_exec_next():
            self.exec_next()

    def exec_next(self):
        """Launch the next reconstruction if any
        """
        if self.empty():
            return
        assert(self.rsyncThread is None or not self.rsyncThread.isRunning())
        self.rsyncThread, callbacks = self.get()
        for callback in callbacks:
            self.rsyncThread.finished.connect(callback)
        self.rsyncThread.start()

    def can_exec_next(self):
        """
        Can we launch an ftserie reconstruction.
        Reconstruction can't be runned in parallel

        :return: True if no reconstruction is actually running
        """
        return self.rsyncThread is None or not self.rsyncThread.isRunning()

    def sync_finisher(self, source, target):
        if hasattr(self, 'rsyncThread'):
            del self.rsyncThread
        self.callback = None
        self.sigQueueFinished.emit(source, target)
        self.exec_next()

    def wait(self, timeout=5):
        for thread in self.threads:
            thread.wait(timeout)


# TODO: remove qt dependency
class _RSyncThread(qt.QThread):
    """Thread dealing with synchronisation
    """

    def __init__(self, source, target, options, parallel):
        qt.QThread.__init__(self)
        self._source = source
        self._target = target
        self._options = options
        self._parallel = parallel

    def run(self):
        if not os.path.exists(self._source):
            logger.info('source folder %s not existing (or no more?)' % self._source)
            return
        command = RSyncManager().get_rsync_command(
            source=self._source,
            target=self._target,
            options=self._options,
            parallel=self._parallel)
        subprocess.call(command, shell=True, stdout=subprocess.PIPE)

        # if delete action have been requested:
        if '--remove-source-files' in self._options:
            if _RSyncThread.remove_empty_folders(self._source) is False:
                mess = 'fail to remove file on %s.' % self._source
                mess += 'Synchronisation might have failed'
                logger.error(mess)

    @staticmethod
    def remove_empty_folders(folder):
        if not(os.path.isdir(folder) and os.path.exists(folder)):
            return True

        assert(os.path.isdir(folder))
        subFiles = os.listdir(folder)

        if len(subFiles) == 0:
            os.rmdir(folder)
        else:
            for subFile in subFiles:
                subFolder = os.path.join(folder, subFile)
                if os.path.isdir(subFolder):
                    if not _RSyncThread.remove_empty_folders(subFolder):
                        return False
                else:
                    return False

            os.rmdir(folder)
        return True


# TODO: remove qt dependency
class _RmThread(qt.QThread):
    """
    Used to remove a set of files if existing
    """
    def __init__(self, source, files_to_rm):
        qt.QThread.__init__(self)
        self.source = source
        self.files_to_rm = files_to_rm

    def run(self):
        for f in self.files_to_rm:
            if os.path.exists(f):
                if os.path.isfile(f):
                    os.remove(f)
                elif os.path.isdir(f):
                    shutil.rmtree(self.dir)
