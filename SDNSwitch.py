from pickle import TRUE
from BlockedUrl import BlockedUrl
from UsomUrlHelper import UsomUrlHelper
import json
import Constants
#-------------------- RYU packages --------------------
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import ethernet, packet, ipv4, ether_types
#-------------------- RYU packages --------------------



class SDNHub(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SDNHub, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.mac_to_port = {}
        self.blocked_url_array = []
        self.load_json()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)
    
    def drop_packets_to_blocked_ip(self):
        pass

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # get Datapath ID to identify OpenFlow switches.
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # get the received port number from packet_in message.
        in_port = msg.match['in_port']

        #self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port
        
        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time.
        if dpid == Constants.FIREWALL_SWITCH_ID:
            for index, blocked_url in enumerate(self.blocked_url_array):
                self.logger.info("added droped packed: %s --- %s", blocked_url.url_name, blocked_url.ip)
                if pkt_ipv4 and (pkt_ipv4.src == blocked_url.ip or pkt_ipv4.dst == blocked_url.ip):
                    default_match_1 = parser.OFPMatch(
                        eth_type=ether_types.ETH_TYPE_IP,
                        ipv4_src=pkt_ipv4.src,
                        ipv4_dst=pkt_ipv4.dst
                    )
                    
                    default_match_2 = parser.OFPMatch(
                        eth_type=ether_types.ETH_TYPE_IP,
                        ipv4_src=pkt_ipv4.dst,
                        ipv4_dst=pkt_ipv4.src
                    )

                    self.add_flow(datapath, index + 3, default_match_1, [])
                    self.add_flow(datapath, index + 2, default_match_2, [])
                    self.logger.info("packet drop: FIREWALL_ID: %s - SRC: %s - DST: %s - URL: %s", dpid, pkt_ipv4.src, pkt_ipv4.dst, blocked_url.url_name)
        elif out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)

    def __load_json(self):
        f = open(Constants.BLOCKED_URL_JSON_FILE_NAME) 
        data = json.load(f)

        for json_data in data:
            blocked_url = BlockedUrl(
                json_data[Constants.URL_NAME],
                json_data[Constants.IP],
                bool(json_data[Constants.IS_ACTIVE])
            )
            self.logger.info("Readed url: %s --- %s", blocked_url.url_name, blocked_url.ip)
            self.blocked_url_array.append(blocked_url)
            self.blocked_url_array = list(filter(lambda x: x.is_active == True, self.blocked_url_array))
        self.logger.info("Blocked url uploaded len: %s", str(len(self.blocked_url_array)))
         
