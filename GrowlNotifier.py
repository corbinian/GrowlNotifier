__version__ = "0.0.1"
__author__ = "Corbinian Bergunde (http://corbinian-bergunde.de)"
__copyright__ = "(C) 2012 Corbinian Bergunde. Code under BSD License."

import sublime,sublime_plugin,traceback


class GrowlNotifier:

    def __init__(self):
        events()

    def sendmessage(self,message):
        import platform
        import os

        Mac = "Darwin"
        Windows = "Windows"
        Linux = "Linux"

        if platform.system() == Mac:
            #Snow Leopard detected
            if platform.release() == "10.8.0":
                self.netgrowlnotification(message)
            #Lion 10.7+  detected
            elif platform.release() >= "10.8.0":
                self.gntpnotification(message)
            #below snow leopard  deteced
            else:
                self.netgrowlnotification(message)


        elif platform.system() == Windows:
                self.gntpnotification(message)

        elif platform.system() == Linux:
                self.gntpnotification(message)

        pass

    def netgrowlnotification(self,message):
        """
        Growl Version:Growl  1.2
        Protocol:UDP
        Note:Growl version 1.2 only works with the old protocol UDP.
        """
        try:
            import netgrowl
            import socket

            PASSWORD = ''
            #create Socket
            addr = ("localhost", netgrowl.GROWL_UDP_PORT)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #register Growl packet
            p = netgrowl.GrowlRegistrationPacket(application='Sublime Text 2', password=PASSWORD)
            p.addNotification()
            sock.sendto(p.payload(), addr)
            #send message
            p = netgrowl.GrowlNotificationPacket(password=PASSWORD, application='Sublime Text 2',
            title="Sublime Text 2", description=message,priority=1,sticky=False)
            sock.sendto(p.payload(), addr)
            #close Socket
            sock.close()
        except Exception as e:
            raise e

    def gntpnotification(self,message):
          """
          Growl Version:Growl  1.3
          Protocol:GNTP
          Note:Growl Version 1.3 works with the new protocol  gntp.
          """
          import gntp.notifier

          try:

            growl = gntp.notifier.GrowlNotifier(
                applicationName = "Sublime Text 2",
                notifications = [title,message],
                )
            growl.register()

            growl.notify(
                noteType = "New Messages",
                title = "Sublime Text 2",
                description = message,
                icon = "https://raw.github.com/dmatarazzo/Sublime-Text-2-Icon/master/st2_icon_128.png",
                sticky = False,
                priority = 1,)

          except Exception as e:
              print e


class events(sublime_plugin.EventListener):



    def on_new(self,view):
        GrowlNotifier().sendmessage("Open new Window")

    def on_clone(self,view):
        GrowlNotifier().sendmessage("View was Cloned")

    def on_load(self,view):
        print view.file_name()
        GrowlNotifier().sendmessage('File: "' + view.file_name() + '" were loaded')

    def on_close(self,view):
        GrowlNotifier().sendmessage("Window were closed")

    def on_post_save(self,view):
        GrowlNotifier().sendmessage('File: "' + view.file_name() +  '" were saved')






events()