import json
import shutil
import time

from cathodic_report.report import Report
from cathodic_report.wordfile import forms


def test_report_render_all(tmp_dir):
    # 这是已有的样例输入文件
    with open("./src/resources/report_form.json", "r", encoding="utf-8") as f:
        report_form = forms.ReportForm.model_validate(json.load(f))

    report = Report(workdir=tmp_dir)
    output = report.render_all(report_form)

    filename = tmp_dir / f"output-{int(time.time())}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output.model_dump(), f, ensure_ascii=False)

    shutil.copyfile(filename, tmp_dir / "output.json")
