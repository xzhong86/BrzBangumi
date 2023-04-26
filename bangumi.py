
import dlSource
import webui

#dlSource.doTest()
lst = dlSource.getList()

for item in lst[:5]:
    print(item)

ui = webui.WebUI()
ui.setDlList(lst)
ui.start(cfg=dict(port=None))

