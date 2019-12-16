from pineapple_nodes.nodes.extraction_nodes import smart_extract_node
from nq import Filter
from pineapple_core.core.node import node, wrap


def test_simple_smart_extract_node():
    x = smart_extract_node("b", 1)
    x.connect_input(iterable={"a": [1, 2, 3], "b": [4, 5, 6]})
    x.trigger()
    assert x["out"].get() == 5


beeg_beeg_dict = {
    "pipelines": [
        {
            "api_name": "beapi_monitoring_github",
            "env": "prd",
            "bus_topic": "beapi_monitoring_github",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/beapi_monitoring_github",
            "short_term_storage_space": "http://a.xyz/beapi_monitoring_github-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": None,
            "dashboard_dev_url": None,
        },
        {
            "api_name": "beapi_whiteapp",
            "env": "prd",
            "bus_topic": "beapi_whiteapp",
            "data_flow_url": None,
            "long_term_storage_space": None,
            "short_term_storage_space": None,
            "short_term_storage_dev_space": "http://a.xyz/beapi_whiteapp-whiteapp*/randomid",
            "dashboard_url": None,
            "dashboard_dev_url": None,
        },
        {
            "api_name": "beapi_monitoring",
            "env": "prd",
            "bus_topic": "beapi_monitoring_prd",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/beapi_monitoring_prd",
            "short_term_storage_space": "http://a.xyz/beapi_monitoring_prd-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "luxbeapi",
            "env": "dev",
            "bus_topic": "luxbeapi_dev",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/luxbeapi_dev",
            "short_term_storage_space": None,
            "short_term_storage_dev_space": "http://a.xyz/luxbeapi_dev-whiteapp*/randomid",
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "luxbeapi",
            "env": "prd",
            "bus_topic": "luxbeapi_prd",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/luxbeapi_prd",
            "short_term_storage_space": "http://a.xyz/luxbeapi_prd-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "luxbeapi",
            "env": "tst",
            "bus_topic": "luxbeapi_tst",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/luxbeapi_tst",
            "short_term_storage_space": "http://a.xyz/luxbeapi_tst-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "luxbeapi",
            "env": "uat",
            "bus_topic": "luxbeapi_uat",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/luxbeapi_uat",
            "short_term_storage_space": "http://a.xyz/luxbeapi_uat-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "sbapi",
            "env": "dev",
            "bus_topic": "sbapi-dev",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/sbapi-dev",
            "short_term_storage_space": "http://a.xyz/sbapi-dev-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "sbapi",
            "env": "prd",
            "bus_topic": "sbapi-prd",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/sbapi-prd",
            "short_term_storage_space": "http://a.xyz/sbapi-prd-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "test_lib_beapi",
            "env": "prd",
            "bus_topic": "test_lib_beapi",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/test_lib_beapi",
            "short_term_storage_space": "http://a.xyz/test_lib_beapi-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": None,
            "dashboard_dev_url": None,
        },
        {
            "api_name": "showroom",
            "env": "prd",
            "bus_topic": "showroom_prd",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/showroom_prd",
            "short_term_storage_space": "http://a.xyz/showroom_prd-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "pingeraas",
            "env": "dev",
            "bus_topic": "pingeraas_dev",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/pingeraas_dev",
            "short_term_storage_space": "http://a.xyz/pingeraas_dev-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "telemetry",
            "env": "dev",
            "bus_topic": "telemetry_dev",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/telemetry_dev",
            "short_term_storage_space": "http://a.xyz/telemetry_dev-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "telemetry",
            "env": "prd",
            "bus_topic": "telemetry_prd",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/telemetry_prd",
            "short_term_storage_space": "http://a.xyz/telemetry_prd-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": "http://a.xyz/app/kibana#/dashboard/randomid",
            "dashboard_dev_url": None,
        },
        {
            "api_name": "whiteapp",
            "env": "prd",
            "bus_topic": "whiteapp_test",
            "data_flow_url": None,
            "long_term_storage_space": "/PRD/DATALAKE/RAW/LOGS_API/whiteapp_test",
            "short_term_storage_space": "http://a.xyz/whiteapp_test-whiteapp*/randomid",
            "short_term_storage_dev_space": None,
            "dashboard_url": None,
            "dashboard_dev_url": None,
        },
    ],
    "_HttpCode": 200,
}


@node(module="Stuff", name="IsWeird")
def weird_node() -> {"api_name": str, "env": str}:
    return wrap({"api_name": "telemetry", "env": "prd"})


def test_advanced_smart_extract_node():
    weird = weird_node()

    pipeline_filter = Filter(
        lambda p: p.value["api_name"] == p.api_name.get()
        and p.value["env"] == p.env.get(),
        "pipeline_filter",
    )

    y = smart_extract_node(
        "pipelines",
        pipeline_filter(api_name=weird["api_name"], env=weird["env"]),
        "dashboard_url",
    )
    y.connect_input(iterable=beeg_beeg_dict)
    weird.trigger()
    y.trigger()
    assert y["out"].get() == "http://a.xyz/app/kibana#/dashboard/randomid"
