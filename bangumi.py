
#import dlSource

import uiDownload
import webui

#dlSource.doTest()
#lst = dlSource.getList()

#for item in lst[:5]:
#    print(item)

#uiDownload.setDlList(lst)

ui = webui.WebUI()
#ui.setDlList(lst)
ui.start(cfg=dict(port=None))
#ui.test(cfg=dict(port=None))

