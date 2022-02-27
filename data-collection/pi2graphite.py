from vcgencmd import Vcgencmd
from datetime import datetime

vcgm = Vcgencmd()

GRAPHITE_URL = ""
GRAPHITE_KEY = ""
GRAPHITE_USER = ""

metrics_to_log = [
	["Temperature",vcgm.measure_temp],
	["Throttled",vcgm.get_throttled],
	["CPU Memory",vcgm.get_mem("arm")],
	["GPU Memory",vcgm.get_mem("gpu")]
	]

def make_metric([name, command]):
	metric = {
	"name": name,
	"interval": 1,
	"metric": name,
	"value": command(),
	"time": int(datetime.now().timestamp())
	}
	return metric

def write_metrics(data):
	data.sort(key=lambda obj: obj["time"])
	try:
		res = requests.post(url,json=data,auth=(GRAPHITE_USER,GRAPHITE_KEY))
	except ConnectionError:
		time.sleep(5)
		res = requests.post(url,json=data,auth=(GRAPHITE_USER,GRAPHITE_KEY))
	print(res)
while True:
	graphite_data_to_send = []
	for metric_to_log in metrics_to_log:
		graphite_data_to_send.append(make_metric(metric_to_log))
	write_metrics(graphite_data_to_send)

