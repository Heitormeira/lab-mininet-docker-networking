#!/usr/bin/env python3
"""
Topologia Mininet — Lab de Rede Corporativa Híbrida

Este script cria uma topologia de rede simulada que demonstra:
- Múltiplos hosts conectados através de switches
- Roteamento entre subnets
- Integração com Docker containers
"""

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import os
import subprocess
import time


class CorpNetTopo(Topo):
    """Topologia de Rede Corporativa"""
    
    def build(self):
        """Construir a topologia"""
        
        # Criar switches
        s1 = self.addSwitch('s1')  # Switch principal - Acesso
        s2 = self.addSwitch('s2')  # Switch secundário - Agregação
        s3 = self.addSwitch('s3')  # Switch de borda
        
        info("✓ Switches criados: s1, s2, s3\n")
        
        # Conectar switches em topologia hierárquica
        self.addLink(s1, s2)  # s1 -> s2
        self.addLink(s2, s3)  # s2 -> s3
        
        # Criar hosts no segmento ADMIN (Subnet: 10.0.0.0/24)
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        
        # Criar hosts no segmento USUARIOS (Subnet: 10.0.1.0/24)
        h3 = self.addHost('h3', ip='10.0.1.1/24')
        h4 = self.addHost('h4', ip='10.0.1.2/24')
        h5 = self.addHost('h5', ip='10.0.1.3/24')
        
        # Criar hosts no segmento SERVIDORES (Subnet: 10.0.2.0/24)
        h6 = self.addHost('h6', ip='10.0.2.1/24')
        h7 = self.addHost('h7', ip='10.0.2.2/24')
        
        info("✓ 7 Hosts criados:\n")
        info("  - Segmento ADMIN: h1, h2 (10.0.0.0/24)\n")
        info("  - Segmento USUARIOS: h3, h4, h5 (10.0.1.0/24)\n")
        info("  - Segmento SERVIDORES: h6, h7 (10.0.2.0/24)\n")
        
        # Conectar hosts aos switches (com latência e bandwidth limitado)
        # S1 - Segmento ADMIN
        self.addLink(h1, s1, bw=100, delay='1ms')  # 100 Mbps, 1ms latência
        self.addLink(h2, s1, bw=100, delay='1ms')
        
        # S2 - Segmento USUARIOS
        self.addLink(h3, s2, bw=100, delay='2ms')
        self.addLink(h4, s2, bw=100, delay='2ms')
        self.addLink(h5, s2, bw=100, delay='2ms')
        
        # S3 - Segmento SERVIDORES
        self.addLink(h6, s3, bw=1000, delay='0.5ms')  # 1 Gbps para servidores
        self.addLink(h7, s3, bw=1000, delay='0.5ms')


def configure_routing(net):
    """Configurar roteamento entre subnets"""
    
    info("\n🔄 Configurando roteamento entre subnets...\n")
    
    # Hosts ADMIN (s1)
    hosts_admin = [net.get('h1'), net.get('h2')]
    for host in hosts_admin:
        host.cmd('ip route add 10.0.1.0/24 via 10.0.0.254')
        host.cmd('ip route add 10.0.2.0/24 via 10.0.0.254')
        info(f"  ✓ {host.name} configurado com rotas para outros segmentos\n")
    
    # Hosts USUARIOS (s2)
    hosts_usuarios = [net.get('h3'), net.get('h4'), net.get('h5')]
    for host in hosts_usuarios:
        host.cmd('ip route add 10.0.0.0/24 via 10.0.1.254')
        host.cmd('ip route add 10.0.2.0/24 via 10.0.1.254')
        info(f"  ✓ {host.name} configurado com rotas para outros segmentos\n")
    
    # Hosts SERVIDORES (s3)
    hosts_servidores = [net.get('h6'), net.get('h7')]
    for host in hosts_servidores:
        host.cmd('ip route add 10.0.0.0/24 via 10.0.2.254')
        host.cmd('ip route add 10.0.1.0/24 via 10.0.2.254')
        info(f"  ✓ {host.name} configurado com rotas para outros segmentos\n")


def start_services(net):
    """Iniciar serviços nos hosts"""
    
    info("\n🚀 Iniciando serviços...\n")
    
    # Iniciar servidor HTTP em h6
    net.get('h6').cmd('cd /tmp && python3 -m http.server 8080 > /tmp/h6_http.log 2>&1 &')
    info("  ✓ Servidor HTTP iniciado em h6 (10.0.2.1:8080)\n")
    
    # Iniciar servidor de eco em h7
    net.get('h7').cmd('nc -l -p 9999 > /tmp/h7_echo.log 2>&1 &')
    info("  ✓ Servidor Echo iniciado em h7 (10.0.2.2:9999)\n")


def show_topology(net):
    """Mostrar informações da topologia"""
    
    info("\n" + "="*60)
    info("TOPOLOGIA DE REDE CORPORATIVA MININET")
    info("="*60 + "\n")
    
    dumpNodeConnections(net.hosts)
    
    info("\n📊 Informações dos Hosts:\n")
    for host in net.hosts:
        info(f"  {host.name}: IP={host.IP()} MAC={host.MAC()}\n")
    
    info("\n💾 Verificar logs dos serviços:\n")
    info("  tail -f /tmp/h6_http.log  (HTTP Server)\n")
    info("  tail -f /tmp/h7_echo.log  (Echo Server)\n")


def main():
    setLogLevel('info')
    
    info("\n" + "="*60)
    info("LAB: Topologia Híbrida Mininet + Docker")
    info("Autor: Heitor Meira | UNICAP")
    info("="*60 + "\n")
    
    # Criar topologia
    topo = CorpNetTopo()
    
    # Criar rede Mininet
    net = Mininet(
        topo=topo,
        controller=Controller,
        switch=OVSSwitch,
        link=TCLink
    )
    
    # Iniciar rede
    info("\n🔌 Iniciando rede Mininet...\n")
    net.start()
    
    # Configurar roteamento
    configure_routing(net)
    
    # Iniciar serviços
    start_services(net)
    
    # Mostrar topologia
    show_topology(net)
    
    info("\n" + "="*60)
    info("COMANDOS ÚTEIS NO CLI:")
    info("="*60)
    info("""
  # Ver informações dos hosts
  mininet> nodes
  mininet> net
  
  # Testar conectividade
  mininet> h1 ping h6
  mininet> h3 ping h7
  
  # Executar testes de throughput
  mininet> h6 iperf -s &
  mininet> h1 iperf -c h6 -t 10
  
  # Acessar shell de um host
  mininet> xterm h1
  
  # Ver tabela de roteamento
  mininet> h1 route
  
  # Capturar tráfego (em outro terminal)
  $ sudo tcpdump -i <interface> -w traffic.pcap
  
  # Sair
  mininet> exit
    """)
    info("\n" + "="*60 + "\n")
    
    # Iniciar CLI interativo
    CLI(net)
    
    # Parar rede
    info("\n🛑 Parando rede...\n")
    net.stop()
    info("✓ Rede parada com sucesso!\n")


if __name__ == '__main__':
    main()
