def test_format():
    assert "device-table-{id}.docx".format(id=1) == "device-table-1.docx"
