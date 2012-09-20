import tornado.websocket
import tornado.web
import tornado.ioloop

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/jabber", JabberHandler),
		]
		settings = dict(
			cookie_secret = "secret",
		)
		tornado.web.Application.__init__(self, handlers, **settings)


class JabberHandler(tornado.websocket.WebSocketHandler):
	waiters = set()

	def allow_draft76(self):
		return True

	def open(self):
		print "Adding client"
		JabberHandler.waiters.add(self)
		self.write_message("Hello")

	def on_close(self):
		print "Removing client"
		JabberHandler.waiters.remove(self)

	def on_message(self, message):
		print "Received message: " + message

def main():
	application = Application()
	application.listen(8081)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
