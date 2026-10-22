# NKZ System Info

Ferramenta de terminal em Python para consultar informações básicas do computador, sem instalar bibliotecas externas.

## Funcionalidades

- Sistema operacional, versão e arquitetura
- Nome do computador e usuário atual
- Processador e quantidade de núcleos lógicos
- Endereço IP local (quando disponível)
- Memória RAM (consulta nativa via API do Windows)
- Espaço total, usado e livre da unidade da pasta atual
- Exportação de relatório em `.txt`

## Requisitos

- Python 3.8 ou superior recomendado
- Nenhuma dependência externa
- Não precisa de `pip`

## Como executar

1. Baixe ou clone este repositório.
2. Abra o terminal na pasta do projeto.
3. Execute:

```bash
python nkz_system_info.py
```

No Windows, se o comando `python` não funcionar, tente:

```bash
py nkz_system_info.py
```

## Observações

- A leitura detalhada da RAM usa `ctypes` e a API nativa `GlobalMemoryStatusEx` do Windows.
- Em sistemas que não sejam Windows, os campos de RAM aparecem como indisponíveis.
- O armazenamento apresentado corresponde à unidade onde a pasta atual está localizada.
- O IP exibido é o endereço associado ao nome do computador; em alguns dispositivos ele pode não ser o IP da interface ativa.
- O programa coleta informações localmente e não envia dados para a internet.

## Estrutura

```text
NKZ-System-Info/
├── nkz_system_info.py
├── README.md
└── .gitignore
```

## Aprendizados

Projeto de estudo para praticar módulos da biblioteca padrão (`os`, `sys`, `platform`, `socket`, `shutil`, `getpass`, `datetime`), funções, tratamento de erros e escrita de arquivos.

## Aviso

Projeto educacional. As informações disponíveis podem variar conforme o sistema operacional e as permissões do usuário.
