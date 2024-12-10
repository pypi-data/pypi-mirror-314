#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2024- MAGO
# AUTHORS:
# Sukbong Kwon (Galois)

"""
Simulator for Mirinae

Usage:
    mirinae user (login | logout | signup | update | delete) [options]
    mirinae plan (create | delete | update | get) [options]
    mirinae sub (create | delete | update | get) [options]
    mirinae adsub (create | delete | update | get) [options]
    mirinae product (create | delete | update | get) [options]
    mirinae project (create | delete | update | get) [options]
    mirinae api (call | call_uri | call_url | dashboard) [options]
    mirinae dashboard (get) [options]
    mirinae pipeline (proj | prod) [options]
    mirinae tool (youtube) [options]
    mirinae -h | --help
    mirinae --version


Common options:
    -h, --help                      Show this message and exit
    --version                       Show version and exit
    --command=<command>             Command to execute (call, call_uri, dashboard, ...)
                                    [default: call]
    --mode=<mode>                   Mode to execute (run, chat, summary, ...)
                                    [default: run]
    --id=<id>                       ID
    -d, --debug                     Debug mode
    -v, --verbose                   Verbose mode
    -n, --name=<name>               Name

Input options:
    --it=<input_type>               Input type (url, uri, file, text, ...)
    -i, --input=<input>             Input
    -a, --audio-path=<path>         Audio file path
    -u, --youtube-url=<youtube_url> Youtube URL
    -t, --text=<text>               Text
    -f, --file=<file>               File path

User options:
    --nologin                       No login
    -e, --email=<email>             Email
    -w, --password=<password>       Password
    --username=<username>           Username
    --nickname=<nickname>           Nickname
    --company=<company>             Company name
    --role=<role>                   Role (admin, user, ...)
    --status=<status>               Status (active, inactive, ...)

Project options:
    --proj-id=<proj_id>             Project ID
    --prod-id=<prod_id>             Product ID

ServicePlan options:
    -p, --plan-name=<plan_name>         Plan name
    -s, --service-name=<service_name>   Service name
    --price=<price>                 Price
                                    [default: 0]
    --currency=<currency>           Currency
                                    [default: KRW]
    --criteria=<criteria>           Criteria
                                    [default: 0]
    --unit=<unit>                   Unit
                                    [default: second]
    --limit=<limit>                 Limit
                                    [default: -1]
    --billing-cycle=<billing_cycle> Billing cycle
                                    [default: Monthly]

Subscription options:
    --get-type=<get_type>           Get type (serviceNames, ...)
    --start-date=<start_date>       Start date
    --end-date=<end_date>           End date
    --next-billing-date=<next_billing_date> Next billing date

API options:
    --media-type=<media_type>       Media type (audio, video, ...)
                                    [default: audio]

Pipeline options:
    --pipeline-path=<pipeline_path> Pipeline path

Subtitles options:
    --num-speakers=<num_speakers>   Number of speakers
                                    [default: 0]

VoiceSeparation options:
    --targets=<targets>             Targets
                                    [default: vocals]

Dashboard options:
    --query=<query>                 Query
"""

# Local
from .utils.set_logging import get_logger
from .utils.show import show_status
from .user import user
from .api.api import api
from .pipeline.pipeline import pipeline
from .dashboard.dashboard import dashboard
from .product.product import product
from .project.project import project


# Define
logger = get_logger(__name__.split('.')[-1])

def main():
    from .utils.parameters import get_params
    params = get_params(__doc__)

    if params.user:
        resp = user(params)   # User management
    if params.api:
        resp = api(params)     # API management
    if params.dashboard:
        resp = dashboard(params)
    if params.pipeline:
        resp = pipeline(params)
    if params.product:
        resp = product(params)
    if params.project:
        resp = project(params)


if __name__ == '__main__':
    main()