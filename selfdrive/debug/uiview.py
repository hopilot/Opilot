#!/usr/bin/env python3
import time

from cereal import car, log, messaging
from common.params import Params
from selfdrive.manager.process_config import managed_processes

if __name__ == "__main__":
  CP = car.CarParams(notCar=True)

  procs = ['camerad', 'modeld']
  for p in procs:
    managed_processes[p].start()

  pm = messaging.PubMaster(['controlsState', 'deviceState', 'pandaStates'])

  msgs = {s: messaging.new_message(s) for s in ['controlsState', 'deviceState']}
  msgs['deviceState'].deviceState.started = True

  msgs['pandaStates'] = messaging.new_message('pandaStates', 1)
  msgs['pandaStates'].pandaStates[0].ignitionLine = True
  msgs['pandaStates'].pandaStates[0].pandaType = log.PandaState.PandaType.uno

  try:
    while True:
      time.sleep(1 / 100)  # continually send, rate doesn't matter
      for s in msgs:
        pm.send(s, msgs[s])
  except KeyboardInterrupt:
    for p in procs:
      managed_processes[p].stop()
