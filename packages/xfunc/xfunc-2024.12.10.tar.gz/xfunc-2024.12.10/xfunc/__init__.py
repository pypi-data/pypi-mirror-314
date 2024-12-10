# /usr/bin/python3
import json,os,time,redis, socket, traceback,sys,builtins, collections,fire
now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))

def consume(modapi:str, name:str=None, func:str=None, host:str='172.17.0.1', port:int=6379, tag='', timeout:int=3, waitms=7200000,  precount=1,  ttl:int=37200, debug=False): 
	''' python xfunc.py hello   '''
	last	= modapi.split('.')[-1]
	if name is None : name = last 
	if func is None : func = last
	r	= redis.Redis(host=host, port=int(port), decode_responses=True)  
	try:
		r.xgroup_create(name, func,  mkstream=True)
	except Exception as e:
		print(e)

	exec(f"from {modapi} import {func}", globals())
	assert func in globals() or "Failed to find the func :" + f"{func}" 
	f = globals()[func] 
	print ( f(), flush=True) # warmup , MUST has the default parameters 

	consumer_name = f'consumer_{socket.gethostname()}_{os.getpid()}'
	processor = os.getenv('processor', consumer_name) + f"-{tag}"
	r.hset(f"info:{name}", f"processor:{processor}", now()) 
	print(f"Started: {consumer_name}|stream={name}|func={func}| ", r,  now(), flush=True)
	while True:
		item = r.xreadgroup(func, consumer_name, {name: '>'}, count=precount, noack=True, block= waitms )
		if not item: break
		if debug: print(f"{name}:\t", item, "\t", now(), flush=True)  
		for stm_arr in item : #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
			for id,arr in stm_arr[1]: 
				try:
					start	= time.time() 
					res		= {'input': arr }
					res['data']	= f({k:json.loads(v) if v.startswith( ('{','[') ) else v for k,v in arr.items()})  # {'snt':'it are ok.'}
					res.update( {"id": str(id), "name":name, "by": processor, "at": now(), "time":round(time.time() - start, 4) })
					r.lpush(f"{name}suc:{id}", json.dumps( res['data'] if 'dataonly' in arr else res)  ) # add dataonly , 2024.12.3
					r.expire(f"{name}suc:{id}", ttl) 
					r.xdel(name, id)  
					r.hincrby(f'called:{name}', processor)  
				except Exception as e:
					print (f"xfunc {name}_process ex:", e, id, arr) 
					r.xdel(name, id)   # added 2024.11.29
					r.lpush(f"{name}err:{id}", json.dumps( dict(arr, **{"e": str(e)}) ))
					r.expire(f"{name}err:{id}", ttl) 
					r.setex(f"exception:{id}", ttl, str(e)) 
					exc_type, exc_value, exc_traceback_obj = sys.exc_info()
					traceback.print_tb(exc_traceback_obj)

	r.xgroup_delconsumer(name, func, consumer_name)
	r.close()
	r.hdel(f'called:{name}', processor)
	print ("Quitted:", consumer_name, "\t",now())

if __name__ == '__main__':
	fire.Fire(consume) 
