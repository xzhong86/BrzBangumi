
import dlSource
import webui

#dlSource.doTest()
lst = dlSource.getList()

for item in lst[:5]:
    print(item)

webui.start(lst, dict(port=None))
