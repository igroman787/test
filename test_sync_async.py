import time
import asyncio
import threading
import multiprocessing

def fac(n):
	if n == 1:
		return 1
	return fac(n - 1) * n
#end define

def work(n):
	#print(f"work {n}")
	for i in range(20000):
		result = fac(n)
	return result
#end define

async def awork(n):
	return work(n)
#end define

def test1():
	#print("start sync code")
	start = time.time()
	result1 = work(910)
	result2 = work(920)
	result3 = work(930)
	diff = time.time() - start
	print(f"sync code take {diff} seconds")
#end define

async def test2():
	#print("start async code")
	start = time.time()
	await awork(910)
	await awork(920)
	await awork(930)
	diff = time.time() - start
	print(f"async code take {diff} seconds")
#end define

def test3():
	#print("start threading code")
	start = time.time()
	t1 = threading.Thread(target=work, args=[910])
	t2 = threading.Thread(target=work, args=[920])
	t3 = threading.Thread(target=work, args=[930])
	t1.start()
	t2.start()
	t3.start()
	t1.join()
	t2.join()
	t3.join()
	diff = time.time() - start
	print(f"threading code take {diff} seconds")
#end define

def test4():
	#print("start multiprocessing code")
	start = time.time()
	p1 = multiprocessing.Process(target=work, args=[910])
	p2 = multiprocessing.Process(target=work, args=[920])
	p3 = multiprocessing.Process(target=work, args=[930])
	p1.start()
	p2.start()
	p3.start()
	p1.join()
	p2.join()
	p3.join()
	diff = time.time() - start
	print(f"multiprocessing code take {diff} seconds")
#end define

def main():
	test1()
	asyncio.run(test2())
	test3()
	test4()
#end define

main()

# Output:
# sync code take 11.847387313842773 seconds
# async code take 11.828837156295776 seconds
# threading code take 20.547234535217285 seconds
# multiprocessing code take 4.018931865692139 seconds
