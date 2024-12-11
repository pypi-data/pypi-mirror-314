#!/usr/bin/env python

# author     : Hadi Cahyadi
# email      : cumulus13@gmail.com
# description: Snarl python lib, Send SNP/3.1 messages. (Snarl)
# created in 37 minutes :)
# -*- coding: UTF-8 -*-

import socket
import sys
import ctraceback
sys.excepthook = ctraceback.CTraceback
import argparse
from pathlib import Path
from configset import configset
import importlib
from rich import print

class Snarl:
    _verbose = False
    CONFIGFILE = Path(__file__).cwd() / 'snarl.ini'
    if not CONFIGFILE.is_file():
        CONFIGFILE = Path(__file__).parent / 'snarl.ini'
    CONFIG = configset(str(CONFIGFILE))
    HOST = '127.0.0.1'
    PORT = 9989

    @classmethod
    def log(self, string):
        if self._verbose: print(string)

    @classmethod
    def send_and_receive(self, ipAddr, port, request, verbose = False):
        if verbose:
            self._verbose = True
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)

        try:
            self.log(f"[bold #FFFF00]Connecting to[/] [bold #FF55FF]{ipAddr}[/]:[bold #00AAFF]{port}[/] ...")
            client.connect((ipAddr, port))

        except socket.timeout:
            self.log(f"[white on red blink]Timed out ![/]")
            self._verbose = False
            return False, "Connection timed out"

        except Exception as e:
            self.log(f"[white on red blink]FAILED ![/]")
            self._verbose = False
            return False, e

        try:
            self.log(f"[bold #FFFF00]Sending...[/]")
            if verbose: print(f"[bold #FF55FF]request xxx:[/] [bold #AAFF7F]{request.decode()}[/]")
            client.send(request)
            self.log(f"[bold #00FFFF]Sent[/]")

        except socket.timeout:
            ctraceback.CTraceback(*sys.exc_info())
            client.close()
            self._verbose = False
            return False, "Timed out sending request"

        except Exception as e:
            ctraceback.CTraceback(*sys.exc_info())
            client.close()
            self._verbose = False
            return False, e
        
        try:
            self.log(f"[bold #FFFF00]Waiting for reply...[/]")
            reply = client.recv(4096)
            self.log(f"[bold #00FFFF]Complete![/]")

        except socket.timeout:
            ctraceback.CTraceback(*sys.exc_info())
            client.close()
            self._verbose = False
            return False, "Timed out waiting for reply"

        except Exception as e:
            ctraceback.CTraceback(*sys.exc_info())
            client.close()
            self._verbose = False
            return False, e

        # completed!
        client.close()
        self._verbose = False
        return True, reply

    @classmethod
    def splitEntry(self, string):
        i = string.find(":")
        if i == -1:
            return "",""

        a = string[0:i].strip()
        b = string[i+1:].strip()
        return a,b

    @classmethod
    def load(self, name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    @classmethod
    def get_version(self):
        if (Path(__file__).cwd() / '__version__.py').is_file():
            try:
                __version__ = self.load('__version__', str(Path(__file__).cwd() / '__version__.py'))
                version = __version__.version
                return version
            except:
                ctraceback.CTraceback(*sys.exc_info())
        elif (Path(__file__).parent / '__version__.py').is_file():
            try:
                __version__ = self.load('__version__', str(Path(__file__).parent / '__version__.py'))
                version = __version__.version
                return version
            except:
                ctraceback.CTraceback(*sys.exc_info())
        
        elif (Path(__file__).parent.parent / '__version__.py').is_file():
            try:
                __version__ = self.load('__version__', str(Path(__file__).parent.parent / '__version__.py'))
                version = __version__.version
                return version
            except:
                ctraceback.CTraceback(*sys.exc_info())
        
    @classmethod
    def send(self, ntype, app_id, title, body, icon = None, host = '127.0.0.1', port = 9989, forward_to = None, priority = None, reply_port = 0, source = None, uid = None, password = None, xheader = {}, data = None , verbose = False):
        if not ntype:
            return {}, False, "ERROR"
        
        host = host or self.CONFIG.get_config('server', 'host') or self.HOST
        port = port or self.CONFIG.get_config('server', 'port') or self.PORT
        x_header = {}

        if data:
            dataKey, dataValue = self.splitEntry(data)
            if dataKey != "" and dataValue != "":
                data[dataKey] = dataValue
        
        if xheader:
            vh = xheader.split(':')
            if len(vh) == 2 and vh[0].strip() != "" and vh[1].strip() != "":
                x_header[vh[0].strip()] = vh[1].strip()

        if ntype in ["NOTIFY", "notify", "n", "N"]:
            request = b"SNP/3.1 " + bytes("NOTIFY", encoding = 'utf-8') + b"\r\n"
            if app_id: request += b"app-id: " + bytes(app_id, encoding = 'utf-8') + b"\r\n"
            if password: request += b"password: " + bytes(password, encoding = 'utf-8') + b"\r\n"
            if title: request += b"title: " + bytes(title, encoding = 'utf-8') + b"\r\n"
            if body: request += b"text: " + bytes(body, encoding = 'utf-8') + b"\r\n"
            if icon: request += b"icon: " + bytes(icon, encoding = 'utf-8') + b"\r\n"
            if uid: request += b"uid: " + bytes(uid, encoding = 'utf-8') + b"\r\n"
            if priority: request += b"priority: " + bytes(priority, encoding = 'utf-8') + b"\r\n"
            if reply_port: request += b"reply-port: " + bytes(str(reply_port), encoding = 'utf-8') + b"\r\n"
            
            if data:
                for key, value in data.items():
                    request += "data-" + key + ": " + value + "\r\n"

            if x_header:
                for key, value in x_header.items():
                    request += "x-" + key + ": " + value + "\r\n"

        elif ntype in ["REGISTER", "register", "r", "R"]:
            request = b"SNP/3.1 " + bytes("REGISTER", encoding = 'utf-8') + b"\r\n"
            if app_id: request += b"app-id: " + bytes(app_id, encoding = 'utf-8') + b"\r\n"
            if title: request += b"title: " + bytes(title, encoding = 'utf-8') + b"\r\n"
            if icon: request += b"icon: " + bytes(icon, encoding = 'utf-8') + b"\r\n"
            if password: request += b"password: " + bytes(password, encoding = 'utf-8') + b"\r\n"

        elif ntype in ["FORWARD", "forward", "f", "F"]:
            request = b"SNP/3.1 " + bytes("FORWARD", encoding = 'utf-8') + b"\r\n"
            if source: request += b"source: " + bytes(source, encoding = 'utf-8') + b"\r\n"
            if password: request += b"password: " + bytes(password, encoding = 'utf-8') + b"\r\n"
            if title: request += b"title: " + bytes(title, encoding = 'utf-8') + b"\r\n"
            if body: request += b"text: " + bytes(body, encoding = 'utf-8') + b"\r\n"
            if icon: request += b"icon: " + bytes(icon, encoding = 'utf-8') + b"\r\n"
            if priority: request += b"priority: " + bytes(priority, encoding = 'utf-8') + b"\r\n"
            if uid: request += b"uid: " + bytes(uid, encoding = 'utf-8') + b"\r\n"
            if reply_port: request += b"reply-port: " + bytes(str(reply_port), encoding = 'utf-8') + b"\r\n"

            if data:
                for key, value in data.items():
                    request += b"data-" + bytes(key, encoding = 'utf-8') + b": " + bytes(value, encoding = 'utf-8') + b"\r\n"

            if xheader:
                for key, value in xheader.items():
                    request += b"x-" + bytes(key, encoding = 'utf-8') + b": " + bytes(value, encoding = 'utf-8') + b"\r\n"

        elif ntype in ["SUBSCRIBE", "subscribe", "s", "S"]:
            request = b"SNP/3.1 " + bytes("SUBSCRIBE", encoding = 'utf-8') + b"\r\n"
            if reply_port:request += b"reply-port: " + bytes(str(reply_port), encoding = 'utf-8') + b"\r\n"
            if forward_to: request += b"forward-to: " + bytes(forward_to, encoding = 'utf-8') + b"\r\n"
            if password: request += b"password: " + bytes(password, encoding = 'utf-8') + b"\r\n"

        request += b"END\r\n"

        if verbose: print(f"[bold #FFAA00]\[{request.strip().decode()}][/]")

        success, reply = self.send_and_receive(host, port, request, verbose)

        if success and verbose:
            print(f"[bold #00AAFF]result:[/] [bold #00FFFF]\[{reply.strip().decode()}][/]")
        elif not success and verbose:
            print(f"[white on red blink]FAILED:[/] [#FFFFFF on #5500FF]{reply.decode()}[/]")

        return request.strip(), success, reply.strip()

    @classmethod
    def usage(self):
        parser = argparse.ArgumentParser(description="Snarl python lib, Send SNP/3.1 messages. (Snarl)")
        parser.add_argument("HOST", help="Target host (IP or hostname). Use '.' for localhost., HOST or PORT can be setup on config file too (snarl.ini)", nargs='?')
        parser.add_argument("PORT", type=int, help="Target port., HOST or PORT can be setup on config file too (snarl.ini)", nargs='?')
        
        parser.add_argument("-N", "--notify", action="store_true", help="Generate NOTIFY message")
        parser.add_argument("-R", "--register", action="store_true", help="Generate REGISTER message")
        parser.add_argument("-F", "--forward", action="store_true", help="Generate FORWARD message")
        parser.add_argument("-S", "--subscribe", action="store_true", help="Generate SUBSCRIBE message")
        
        parser.add_argument("-a", "--app-id", help="Application ID (R, N)")
        parser.add_argument("-b", "--body", help="Notification body (F, N)")
        parser.add_argument("-d", "--data", action="append", help="Data-* entry (F, N), format key:value")
        parser.add_argument("-f", "--forward-to", help="Forward-to (F, N, S)")
        parser.add_argument("-i", "--icon", help="Icon (F, N, R)")
        parser.add_argument("-p", "--priority", help="Priority (F, N)")
        parser.add_argument("-r", "--reply-port", type=int, help="Reply port (F, N, S)")
        parser.add_argument("-s", "--source", help="Source (F)")
        parser.add_argument("-t", "--title", help="Title (F, N, R)")
        parser.add_argument("-u", "--uid", help="UID (F, N)")
        parser.add_argument("-w", "--password", help="Password (F, N, R, S)")
        parser.add_argument("-x", "--x-header", action="append", help="X-* header (F, N), format key:value")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
        parser.add_argument("-V", "--version", action="store_true", help="Get version number")

        if len(sys.argv) == 1:
            parser.print_help()
        elif sys.argv[1] in ['-V', '--version']:
            print(
                f"[bold #00FFFF]snarl (python lib)[/], " \
                f"[bold #AAFF00]{'version: ' + str(self.get_version()) if self.get_version() else ''}[/]\n"\
                f"[bold #FFAAFF]Copyright (c)[/] [bold #FFAA00]2024[/] [bold #FFFF00]Hadi Cahyadi[/] "\
                f"[bold #00AAFF](cumulus13@gmail.com)[/]"
            )
            sys.exit()
        else:
            args = parser.parse_args()

            if args.version:
                print(
                    f"[bold #00FFFF]snarl (python lib)[/], " \
                    f"[bold #AAFF00]{'version: ' + str(self.get_version()) if self.get_version() else ''}[/]\n"\
                    f"[bold #FFAAFF]Copyright (c)[/] [bold #FFAA00]2024[/] [bold #FFFF00]Hadi Cahyadi[/] "\
                    f"[bold #00AAFF](cumulus13@gmail.com)[/]"
                )
                sys.exit()

            if (not args.HOST and not args.PORT) and (not self.CONFIG.get_config('server', 'host') and not self.CONFIG.get_config('server', 'port')):
                parser.print_help()
                print(f"\n[white on red blink]Please input HOST and PORT or you can setup on config file too (snarl.ini) ![/]")
                sys.exit()

            # data = { }
            # xheader = { }
            HOST = args.HOST or self.CONFIG.get_config('server', 'host')
            PORT = int(args.PORT or self.CONFIG.get_config('server', 'port'))

            # dataKey, dataValue = "",""
            if HOST in [".", "0.0.0.0", "::1"]: HOST = '127.0.0.1'

            message_type = ""
            if args.notify:
                message_type = "NOTIFY"
            elif args.register:
                message_type = "REGISTER"
            elif args.forward:
                message_type = "FORWARD"
            elif args.subscribe:
                message_type = "SUBSCRIBE"
            
            # if args.data:
            #     dataKey,dataValue = self.splitEntry(args.data)
            #     if dataKey != "" and dataValue != "":
            #         data[dataKey] = dataValue
            
            # if args.x_header:
            #     vh = args.x_header.split(':')
            #     if len(vh) == 2 and vh[0].strip() != "" and vh[1].strip() != "":
            #         xheader[vh[0].strip()] = vh[1].strip()

            # if args.notify:
            #     request = b"SNP/3.1 " + bytes("NOTIFY", encoding = 'utf-8') + b"\r\n"
            #     if args.app_id:
            #         request += b"app-id: " + bytes(args.app_id, encoding = 'utf-8') + b"\r\n"

            #     if args.password:
            #         request += b"password: " + bytes(args.password, encoding = 'utf-8') + b"\r\n"

            #     if args.title:
            #         request += b"title: " + bytes(args.title, encoding = 'utf-8') + b"\r\n"

            #     if args.body:
            #         request += b"text: " + bytes(args.body, encoding = 'utf-8') + b"\r\n"

            #     if args.icon:
            #         request += b"icon: " + bytes(args.icon, encoding = 'utf-8') + b"\r\n"

            #     if args.uid:
            #         request += b"uid: " + bytes(args.uid, encoding = 'utf-8') + b"\r\n"

            #     if args.priority:
            #         request += b"priority: " + bytes(args.priority, encoding = 'utf-8') + b"\r\n"

            #     if args.reply_port:
            #         request += b"reply-port: " + bytes(str(args.reply_port), encoding = 'utf-8') + b"\r\n"

            #     if data:
            #         for key, value in data.items():
            #             request += "data-" + key + ": " + value + "\r\n"

            #     if xheader:
            #         for key, value in xheader.items():
            #             request += "x-" + key + ": " + value + "\r\n"

            # elif args.register:
            #     request = b"SNP/3.1 " + bytes("REGISTER", encoding = 'utf-8') + b"\r\n"
            #     if args.app_id:
            #         request += b"app-id: " + bytes(args.app_id, encoding = 'utf-8') + b"\r\n"

            #     if args.title:
            #         request += b"title: " + bytes(args.title, encoding = 'utf-8') + b"\r\n"

            #     if args.icon:
            #         request += b"icon: " + bytes(args.icon, encoding = 'utf-8') + b"\r\n"

            #     if args.password:
            #         request += b"password: " + bytes(args.password, encoding = 'utf-8') + b"\r\n"

            # elif args.forward:
            #     request = b"SNP/3.1 " + bytes("FORWARD", encoding = 'utf-8') + b"\r\n"

            #     if args.source:
            #         request += b"source: " + bytes(args.source, encoding = 'utf-8') + b"\r\n"

            #     if args.password:
            #         request += b"password: " + bytes(args.password, encoding = 'utf-8') + b"\r\n"

            #     if args.title:
            #         request += b"title: " + bytes(args.title, encoding = 'utf-8') + b"\r\n"

            #     if args.body:
            #         request += b"text: " + bytes(args.body, encoding = 'utf-8') + b"\r\n"

            #     if args.icon:
            #         request += b"icon: " + bytes(args.icon, encoding = 'utf-8') + b"\r\n"

            #     if args.priority:
            #         request += b"priority: " + bytes(args.priority, encoding = 'utf-8') + b"\r\n"

            #     if args.uid:
            #         request += b"uid: " + bytes(args.uid, encoding = 'utf-8') + b"\r\n"

            #     if args.reply_port:
            #         request += b"reply-port: " + bytes(str(args.reply_port), encoding = 'utf-8') + b"\r\n"

            #     if data:
            #         for key, value in data.items():
            #             request += b"data-" + bytes(key, encoding = 'utf-8') + b": " + bytes(value, encoding = 'utf-8') + b"\r\n"

            #     if xheader:
            #         for key, value in xheader.items():
            #             request += b"x-" + bytes(key, encoding = 'utf-8') + b": " + bytes(value, encoding = 'utf-8') + b"\r\n"

            # elif args.subscribe:
            #     request = b"SNP/3.1 " + bytes("SUBSCRIBE", encoding = 'utf-8') + b"\r\n"

            #     if args.reply_port:
            #         request += b"reply-port: " + bytes(str(args.reply_port), encoding = 'utf-8') + b"\r\n"

            #     if args.forward:
            #         request += b"forward-to: " + bytes(args.forward, encoding = 'utf-8') + b"\r\n"

            #     if args.password:
            #         request += b"password: " + bytes(args.password, encoding = 'utf-8') + b"\r\n"

            # request += b"END\r\n"

            # if args.verbose: print(f"[bold #FFAA00]\[{request.strip().decode()}][/]")

            if args.notify or args.register or args.forward or args.subscribe:
                self.send(message_type, args.app_id, args.title, args.body, args.icon, HOST, PORT, args.forward_to, args.priority, args.reply_port, args.source, args.uid, args.password, args.x_header, args.data, args.verbose)

                # success, reply = self.send_and_receive(HOST, PORT, request)

                # if success:
                #     print(f"[bold #00AAFF]result:[/] [bold #00FFFF]\[{reply.strip().decode()}][/]")
                # else:
                #     print(f"[white on red blink]FAILED:[/] [#FFFFFF on #5500FF]{reply.decode() if hasattr(reply, 'decode') else reply}[/]")
            else:
                parser.print_help()

if __name__ == '__main__':
    Snarl.usage()