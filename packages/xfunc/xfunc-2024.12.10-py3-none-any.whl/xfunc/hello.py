# sample code,  funcname = filename
import time

def hello( arr:dict={"one":"two"}):
	return dict(arr, **{"by": "hello", "at": time.time()})

if __name__ == '__main__':
	print ( hello()) 
