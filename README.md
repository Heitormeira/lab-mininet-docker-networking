# Lab Topologia Híbrida — Mininet + Docker

> Simulação de rede corporativa híbrida combinando **Mininet** (simulação de rede) com **Docker** (containerização)

## 📋 Objetivo

Este laboratório demonstra na prática como:
- **Redes corporativas** são arquitetadas com múltiplos segmentos
- **Containers Docker** se comunicam através de diferentes tipos de redes
- **Tráfego de rede** é analisado em um ambiente controlado
- **Conceitos de IP, roteamento e switching** funcionam na prática

## 🏗️ Topologia

```
┌─────────────────────────────────────────────────────────────┐
│                      MININET NETWORK                         │
│                                                              │
│  Host A (10.0.0.1)  ──┐                     ┌── Host B (10.0.0.2)
│                       │                     │
│  Host C (10.0.0.3)  ──┤──  Switch S1  ──┬──┤
│                       │                  │  └── Host D (10.0.0.4)
│  Host E (10.0.0.5)  ──┘                 │
│                                    Switch S2  (Conecta ao Docker)
│                                        │
└─────────────────────────────────────────┼────────────────────┘
                                          │
┌─────────────────────────────────────────┼────────────────────┐
│                  DOCKER NETWORK                             │
│                                        │                    │
│   Container Web (172.18.0.2)  ←─────────                   │
│                                                              │
│   Container DB (172.18.0.3)                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Versão | Propósito |
|-----------|--------|----------|
| **Mininet** | 2.3+ | Simulação de rede |
| **Docker** | 20.10+ | Containerização |
| **Docker Compose** | 1.29+ | Orquestração de containers |
| **Python** | 3.8+ | Scripts de automação |
| **Linux** | Ubuntu 20.04+ | Sistema operacional |
| **iperf3** | 3.0+ | Teste de throughput/latência |

## 📦 Pré-requisitos

```bash
# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar Mininet
sudo apt install mininet -y

# Instalar Docker
sudo apt install docker.io docker-compose -y

# Adicionar usuário ao grupo docker (evitar sudo)
sudo usermod -aG docker $USER
newgrp docker

# Instalar ferramentas de teste
sudo apt install iperf3 net-tools curl wget -y

# Instalar Python e dependências
sudo apt install python3 python3-pip -y
pip install scapy paramiko
```

## 🚀 Como Executar

### 1. Clonar o Repositório

```bash
git clone https://github.com/heitormeira/lab-mininet-docker-networking.git
cd lab-mininet-docker-networking
```

### 2. Configurar o Ambiente

```bash
# Dar permissão de execução aos scripts
chmod +x scripts/*.py
chmod +x scripts/setup.sh

# Executar setup inicial
sudo ./scripts/setup.sh
```

### 3. Iniciar o Mininet

```bash
# Executar o topologia Mininet com Python
sudo python3 topologia_mininet.py
```

**Isso abrirá o CLI do Mininet.** Você verá:
```
mininet> 
```

### 4. Em outro terminal, Iniciar Docker

```bash
# Subir os containers
docker-compose up -d

# Verificar containers rodando
docker ps
docker network ls
```

### 5. Testar Conectividade

No CLI do Mininet, teste:

```bash
# Pingar entre hosts simulados
mininet> h1 ping h2
mininet> h1 ping h3

# Checar IP de cada host
mininet> h1 ifconfig
mininet> h2 ifconfig

# Acessar container do Docker a partir do Mininet
mininet> h1 ping <IP_DOCKER_CONTAINER>

# Testar throughput entre hosts
mininet> h1 iperf -s &
mininet> h2 iperf -c h1 -t 10
```

### 6. Analisar Tráfego com tcpdump

Em um terceiro terminal:

```bash
# Capturar tráfego na interface virtual
sudo tcpdump -i <interface_name> -w capture.pcap

# Depois, abrir no Wireshark
wireshark capture.pcap
```

## 📊 Estrutura do Projeto

```
lab-mininet-docker-networking/
├── README.md                  # Este arquivo
├── topologia_mininet.py       # Script que cria a topologia Mininet
├── docker-compose.yml         # Orquestração dos containers
├── scripts/
│   ├── setup.sh              # Script de setup inicial
│   ├── test_connectivity.py  # Testes automatizados
│   └── analyze_traffic.py    # Análise de tráfego
├── dockerfiles/
│   ├── Dockerfile.web        # Imagem do servidor web
│   └── Dockerfile.db         # Imagem do servidor de BD
├── docs/
│   ├── CONCEITOS.md          # Conceitos de rede explicados
│   ├── TOPOLOGIA.md          # Detalhes da topologia
│   └── TROUBLESHOOTING.md    # Soluções de problemas
└── logs/
    └── trafego.pcap          # Captura de tráfego (gerado)
```

## 🔍 Conceitos Demonstrados

### 1. **Arquitetura de Redes**
- Topologia em árvore com múltiplos switches
- Segmentação de rede (subnets)
- Roteamento entre segmentos

### 2. **Virtualização & Containerização**
- Criação de hosts virtuais com Mininet
- Containers Docker em rede isolada
- Comunicação entre container e rede simulada

### 3. **Networking no Docker**
- Tipos de rede: bridge, host, overlay
- Docker Compose para multi-container
- DNS interno do Docker

### 4. **Linux Networking**
- Configuração de interfaces (ifconfig, ip)
- Roteamento (route, ip route)
- Firewall e iptables
- Network namespaces

### 5. **Testes de Rede**
- Ping e ICMP
- TCP/UDP com iperf
- Análise de tráfego com tcpdump
- Rastreamento de rotas (traceroute)

## 📈 Resultados Esperados

Após executar este lab, você conseguirá:

✅ Criar uma topologia de rede customizada  
✅ Simular múltiplos hosts com endereços IP distintos  
✅ Executar Docker containers em rede isolada  
✅ Testar comunicação entre hosts simulados e containers  
✅ Medir latência, bandwidth e jitter  
✅ Capturar e analisar pacotes de rede  
✅ Compreender fluxo de dados em rede  

## 🐛 Troubleshooting

### Erro: "Permission denied" ao executar topologia_mininet.py
```bash
# Solução: executar com sudo
sudo python3 topologia_mininet.py
```

### Erro: "Docker daemon is not running"
```bash
# Solução: iniciar o Docker
sudo systemctl start docker
```

### Containers não conseguem pingar hosts do Mininet
- Verificar se ambas as redes estão configuradas
- Checar rotas com `docker exec <container> ip route`
- Verificar firewall/iptables

Veja mais em `docs/TROUBLESHOOTING.md`

## 📚 Referências

- [Mininet Walkthrough](http://mininet.org/walkthrough/)
- [Docker Networking](https://docs.docker.com/network/)
- [TCP/IP Protocol Stack](https://en.wikipedia.org/wiki/Internet_protocol_suite)
- [Linux Network Namespaces](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)

## 👨‍💻 Autor

**Heitor Meira** — Estudante de Ciência da Computação  
UNICAP — Pernambuco, Brasil

## 📄 Licença

Este projeto está sob a licença MIT. Veja `LICENSE` para detalhes.

---

**Última atualização:** Agosto 2025  
**Status:** ✅ Em desenvolvimento & testes
