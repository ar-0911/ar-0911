# Aditya Ramguru

**Infrastructure & platform engineer** · zero-trust networking · cloud security · AI developer platforms

I'm a Software Engineer at Aurm, a secure wealth-storage startup in Bangalore, where I'm the sole infrastructure engineer and report directly to the CTO. I own our zero-trust network, cloud security and compliance, observability, and the AI developer platform every engineer builds on, across AWS and GCP.

I like working out how many users a system can take, where it breaks, and which pieces fit best. The cloud never really ends, and that's the fun part.

### What I've built

- **Zero-trust edge network.** A WireGuard/VyOS hub-and-spoke mesh connecting 30+ edge nodes to AWS, with automated peer registration and domain-based split tunneling (dnsmasq, ipset, iptables policy routing).
- **Identity-based access.** HA Teleport (DynamoDB-backed) exposing 120 internal apps across the edge fleet, layered behind Cloudflare WARP for defense in depth. Wrote a retry patch for Teleport's application tunnel client, being prepared for upstream.
- **Cloudflare networking as code.** Tunnels, virtual networks, split tunnels and Cloudflare Mesh across AWS and GCP, codified as Terraform modules; moved public load balancers behind Cloudflare Tunnel + Access.
- **AI developer platform.** A LiteLLM gateway on ECS Fargate + RDS routing Claude Code to AWS Bedrock for 50 users with org and per-user budgets. Claude Code skills and subagents used by every developer, so 100% of PRs are agent-driven.
- **Security & compliance.** Cut Trivy findings from 83 critical/high to 3 (96%), enforced read-only root filesystems across production ECS services to clear a third-party cloud security audit, and automated AWS Security Hub remediation.
- **Observability.** Self-hosted Mimir / Loki / Grafana / Alloy on AWS with S3-backed storage and self-healing ASGs, monitoring the whole edge fleet.

### Stack

![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare_Zero_Trust-F38020?style=flat-square&logo=cloudflare&logoColor=white)
![WireGuard](https://img.shields.io/badge/WireGuard-88171A?style=flat-square&logo=wireguard&logoColor=white)
![Teleport](https://img.shields.io/badge/Teleport-512FC9?style=flat-square)
![Grafana](https://img.shields.io/badge/Grafana_LGTM-F46800?style=flat-square&logo=grafana&logoColor=white)
![Wazuh](https://img.shields.io/badge/Wazuh-3595F9?style=flat-square)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-5FA04E?style=flat-square&logo=nodedotjs&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=flat-square&logo=claude&logoColor=white)

### Background

- B.Tech in Computer Science (Bioinformatics), VIT Vellore, 2021–2025 · CGPA 9.53/10 · merit scholar all four years
- AWS Certified Solutions Architect – Associate
- Academic intern at NUS Singapore (2023–24): led a six-person team building Verdict Hub, a legal-outcome prediction model deployed on AWS SageMaker

### Get in touch

[![Email](https://img.shields.io/badge/aditya.ramguru@gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:aditya.ramguru@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aditya-ramguru-995423218/)
