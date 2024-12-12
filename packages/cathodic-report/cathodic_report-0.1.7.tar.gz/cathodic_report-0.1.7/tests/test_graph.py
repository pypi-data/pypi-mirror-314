from cathodic_report import graph


def test_device_table():
    table = graph.DeviceTable(
        table_name="测试表格",
        c_type="交流",
        start_time="2023-01-01 00:00:00",
        end_time="2023-01-01 23:59:59",
        total_time=86400,
        po=graph.StaticValue(min=-0.95, max=-0.85, mean=-0.90),
        pf=graph.StaticValue(min=-0.92, max=-0.82, mean=-0.87),
        dc_density=graph.StaticValue(min=0.8, max=1.2, mean=1.0),
        ac_density=graph.StaticValue(min=0.9, max=1.3, mean=1.1),
        ac_voltage=graph.StaticValue(min=0.5, max=0.9, mean=0.7),
        judge_result="高",
    )

    with open("./tmp/table.json", "w", encoding="utf-8") as f:
        f.write(table.model_dump_json())
