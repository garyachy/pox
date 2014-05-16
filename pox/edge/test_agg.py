# Copyright 2012,2013 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Testing port mod
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
import time

log = core.getLogger()

def _handle_ConnectionUp (event):
  con = event.connection

  log.debug("_handle_ConnectionUp: %i ports", len(con.ports))

def _handle_PortStatus (event):
  print event.ofp
  log.debug("_handle_PortStatus: %i port", event.port)

def _handle_FlowStats (event):
  bytes = 0
  flows = 0

  for f in event.stats:
    bytes += f.byte_count
    flows += 1

  log.info("Traffic: %s bytes over %s flows", bytes, flows)

def _timer_func ():
  for connection in core.openflow._connections.values():
    connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def launch ():
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  core.openflow.addListenerByName("PortStatus", _handle_PortStatus)
  core.openflow.addListenerByName("FlowStatsReceived", _handle_FlowStats)

  Timer(5, _timer_func, recurring=True)




