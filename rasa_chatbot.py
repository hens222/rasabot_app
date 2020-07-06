from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
app.run()

#from __future__ import absolute_import
#from __future__ import division
#from __future__ import print_function
#from __future__ import unicode_literals
#
#import logging
#import rasa_core
#from rasa_core.agent import Agent
#from rasa_core.policies.keras_policy import KerasPolicy
#from rasa_core.policies.memoization import MemoizationPolicy
#from rasa_core.interpreter import RasaNLUInterpreter
#from rasa_core.utils import EndpointConfig
#from rasa_core.run import serve_application
#from rasa_core import config
#
#from rasa_core.policies.fallback import FallbackPolicy
#from rasa_core.policies.keras_policy import KerasPolicy
#
#from flask import Flask
#from flask_cors import CORS, cross_origin
#
#app = Flask(__name__)
#CORS(app)
#
#logger = logging.getLogger(__name__)
#
#def rasa_agent():
#    interpreter = RasaNLUInterpreter("Path for NLU")
#    action_endpoint = EndpointConfig(url="Webhook URL")
#    agent = Agent.load('Path to Dialogue', interpreter=interpreter, action_endpoint=action_endpoint)
#    ## Next line runs the rasa in commandline
#    # rasa_core.run.serve_application(agent,channel='cmdline') 
#    return agent
#
#@app.route("/conversations/default/respond",methods=['POST'])
#def run_weather_bot(serve_forever=True):
#
#    agent = rasa_agent() # calling rasa agent
#    ## Collect Query from POST request
#    ## Send Query to Agent
#    ## Get Response of BOT
#    output = {} ## Append output
#    return jsonify(output) 
#
#if __name__ == '__main__':
#
#    app.run("xxx.xx.xx.xxx",5005,debug=True)
