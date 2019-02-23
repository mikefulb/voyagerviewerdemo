#
# voyagerviewerdemo - monitor Voyager application server and display images
#
# Copyright 2019 Michael Fulbright
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import json
import logging

from PyQt5 import QtNetwork, QtCore


class VoyagerClientSignals(QtCore.QObject):
        new_fit_ready = QtCore.pyqtSignal(object)
        signal = QtCore.pyqtSignal(int)
        shutdown = QtCore.pyqtSignal()

        # FIXME we should get this down to just a single signal
        # to indicate connection is lost
        tcperror = QtCore.pyqtSignal()
        connect_close = QtCore.pyqtSignal(int)
        disconnected = QtCore.pyqtSignal()

class VoyagerClient:

    def __init__(self):
        self.socket = None
        self.requests = {}
        self.request_id = 0
        self.connected = False
        self.signals = VoyagerClientSignals()

    def connect(self):
        if self.socket:
            logging.warning('VoyagerClient:connect() socket appears to be active already!')

        # FIXME Need some error handling!
        self.socket = QtNetwork.QTcpSocket()

        logging.info('Connecting')

        # FIXME Does this leak sockets?  Need to investigate why
        # setting self.socket = None causes SEGV when disconnected
        # (ie PHD2 closes).
        self.socket.connectToHost('127.0.0.1', 5950)

        logging.info('waiting')

        # should be quick so we connect synchronously
        if not self.socket.waitForConnected(5000):
            logging.error('Could not connect to Voyager')
            self.socket = None
            return False

        self.connected = True

        self.socket.readyRead.connect(self.process)
        self.socket.error.connect(self.error)
        self.socket.stateChanged.connect(self.state_changed)
        self.socket.disconnected.connect(self.disconnected)

        return True

    def disconnect(self):
        if not self.connected:
             logging.warning('VoyagerClient:disconnect() socket appears to be inactive already!')
             return False

        try:
            self.socket.disconnectFromHost()
        except Exception as e:
            logging.error('Exception VoyagerClient:disconnect()!', exc_info=True)
            return False

        self.connected = False
        return True

    def is_connected(self):
        return self.connected

    #
    # FOR REFERENCE - I have found setting self.socket to None causes SEGV when
    #                 the other end has disconnected (like you close PHD2)
    #
    #                 All I can guess is by setting it to None it causes
    #                 a C++ destructor(?) to do bad things in the library
    #
    #                 To counter this I use self.connected to indicate if
    #                 the connection is up.
    #
    def disconnected(self):
        logging.info('disconnected signal from socket!')

        self.connected = False
        self.signals.disconnected.emit()

    def state_changed(self, state):
        logging.info(f'socket state_changed -> {state}')
        # FIXME is this only error we need to catch?
        if state == QtNetwork.QAbstractSocket.ClosingState or \
            state == QtNetwork.QAbstractSocket.UnconnectedState:
                if self.connected:
                    self.connected = False
#                    self.socket = None
                    self.signals.connect_close.emit(state)

    def error(self, socket_error):
        logging.error(f'VoyagerClient:error called! socket_error = {socket_error}')
        self.signals.tcperror.emit()

    def process(self):
        """See if any data has arrived and process"""

#        logging.info('processing')

        if not self.socket:
            logging.error('VoyagerClient:process PHD2 not connected!')
            return False

        while True:
            resp = self.socket.readLine(2048)

            if len(resp)<1:
                break

#            logging.info(f'{resp}')

            try:
                j = json.loads(resp)

                logging.info(f'j->{j}')

                # is this a resonse to a request?
                if 'Event' in j:
                    try:
                        event = j['Event']
                        timestamp = j['Timestamp']
                        host = j['Host']
                        inst = j['Inst']
                    except KeyError as e:
                        logging.error(f'Error parsing field key {e} from event \'{event}\' : json record = {j}')
                        continue

                    logging.info(f'Event Type \'{event}\':')
                    logging.info(f'\tTimestamp: {timestamp}')
                    logging.info(f'\tHost: {host}')
                    logging.info(f'\tInst: {inst}')
                    if event == 'Version':
                        try:
                            voy_vers = j['VOYVersion']
                            voy_subvers = j['VOYSubver']
                            msg_vers = j['MsgVersion']
                        except KeyError as e:
                            logging.error(f'Error parsing field key {e} from event \'{event}\' : json record = {j}')
                            continue
                        logging.info(f'\tVOYVersion: {voy_vers}')
                        logging.info(f'\tBOYSubver: {voy_subvers}')
                        logging.info(f'\tMsgVersion: {msg_vers}')
                        self.send_polling_response(j)
                    elif event == 'Polling':
                        logging.info(f'Event Type {event}:')
                        logging.info('Sending client response')
                        self.send_polling_response(j)
#                        cmd = j
#                        return self.__send_json_command(cmd)
                    elif event == 'Signal':
                        try:
                            code = j['Code']
                        except KeyError as e:
                            logging.error(f'Error parsing field key {e} from event \'{event}\' : json record = {j}')
                            continue
                        logging.info(f'\tCode: {code}')
                        self.signals.signal.emit(code)
                        self.send_polling_response(j)
                    elif event == 'NewFITReady':
                        try:
                            filename = j['File']
                            filetype = j['Type']
                        except KeyError as e:
                            logging.error(f'Error parsing field key {e} from event \'{event}\' : json record = {j}')
                            continue
                        logging.info(f'\tFile: {filename}')
                        logging.info(f'\tType: {filetype}')
                        self.signals.new_fit_ready.emit((filename, filetype))
                        self.send_polling_response(j)
                    elif event == 'Shutdown':
                        self.signals.shutdown.emit()
                    else:
                        logging.warning(f'Event Type {event}: UNHANDLED!')

                    continue
                else:
                    logging.warning(f'Event received with no \'Event\' key - json record = {j}')
                    continue

            except Exception as e:
                logging.error(f'voyager_process - exception message was {resp}!')
                logging.error('Exception ->', exc_info=True)
                continue

        return True

    def __send_json_request(self, req):
        self.requests[self.request_id] = req
        reqdict = {}
        reqdict['method'] = req
        reqdict['id'] = self.request_id
        self.request_id += 1

        cmdstr = json.dumps(reqdict) + '\r\n'
        if 'app_state' not in req:
            logging.info(f'jsonrequest->{bytes(cmdstr, encoding="ascii")}')

        if not self.connected:
            logging.warning('__send_json_request: not connected!')
            return False
            return

        # FIXME this isnt good enough - could be set to None before
        # we actually get to writing
        # need locking?
        try:
            logging.info(f'__send_json_request: cmdstr = {cmdstr}')

            self.socket.writeData(bytes(cmdstr, encoding='ascii'))
        except Exception as e:
            logging.error(f'__send_json_request - req was {req}!')
            logging.error('Exception ->', exc_info=True)
            return False

        return True

    # given a received json for an event send a polling response to reset timer
    def send_polling_response(self, event):
        logging.info(f'sending_polling_response for event {event}')
        poll_cmd = {}
        poll_cmd['Event'] = 'Polling'
        poll_cmd['Timestamp'] = event['Timestamp']
        poll_cmd['Host'] = event['Host']
        poll_cmd['Inst'] = event['Inst']
        return self.__send_json_command(poll_cmd)

    def __send_json_command(self, cmd):
        cmd['id'] = self.request_id
        self.request_id += 1

        cmdstr = json.dumps(cmd) + '\r\n'
        logging.info(f'jsoncmd->{bytes(cmdstr, encoding="ascii")}')

        # FIXME this isnt good enough - could be set to None before
        # we actually get to writing
        # need locking?
        if not self.connected:
            logging.warning('__send_json_command: not connected!')
            return False

        try:
            logging.info(f'__send_json_command: cmdstr = {cmdstr}')
            self.socket.writeData(bytes(cmdstr, encoding='ascii'))
        except Exception as e:
            logging.error(f'__send_json_command - cmd was {cmd}!')
            logging.error('Exception ->', exc_info=True)
            return False

        return True

# TESTING ONLY
p = None

def new_fits(fname, ftype):
    logging.info(f'new_fits: {fname} {ftype}')

def connect_voyager():
    global p
    p = VoyagerClient()

    if not p.connect():
        logging.error('Could not connec to Voyager!')
        sys.exit(-1)

    p.signals.new_fit_ready.connect(new_fits)


if __name__ == '__main__':

    logging.basicConfig(filename='VoyagerClient.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # add to screen as well
    log = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)

    logging.info('VoyagerClient Test Mode starting')

    app = QtCore.QCoreApplication(sys.argv)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        logging.info('starting event loop')

        # connect 1 second after starting main loop
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(connect_voyager)
        timer.start(1000)

        QtCore.QCoreApplication.instance().exec_()


