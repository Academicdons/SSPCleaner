import sys
import os
import time


class FB_WhatsappLinksBot(object):
    def countLinks(self):
        with open(self.get_path('resources\\whatsAppUrls.txt'), 'r') as file:
            self.line_counter = 0
            for line in file:
                if line != "\n":
                    self.line_counter += 1
            file.close()
        return(self.line_counter)
        

    def init(self):
        self.start_time = time.time()
        try:
            with open(self.get_path('resources\\docs\\mydocs.txt'), 'a') as f:
                f.truncate(0)
        finally:
            pass
        with open(self.get_path('resources\\whatsAppUrls.txt'), 'r') as file:
            self.line_count = 0
            for line in file:
                if line != "\n":
                    self.line_count += 1
            file.close()
        print(f'working with over {self.line_count} Links')
        # if self.line_count > 1000:
        #     self.urlCountperDoc = 500
        # else:
        #     if self.line_count >= 10000:
        #         self.urlCountperDoc = 1000
        #     else:
        #         if self.line_count <= 100:
        #             self.urlCountperDoc = self.line_count
        # print(f'line count per doc will be {self.line_count}')
        self.docNumber = 0
        self.cleanlinks()

    def cleanlinks(self):
        if self.countLinks() == 0:
            with open(self.get_path('resources\\docs\\mydocs.txt'), 'a') as f:
                f.write('No Links collected')
            print('Done manupilating links in', "--- %s seconds ---" % (time.time() - self.start_time))
            os._exit(0)
            # sys.exit(0)

        self.docLists = []
        self.docNumber += 1
        doc = f'linkDoc{self.docNumber}.txt'
        try:
            with open(self.get_path('resources\\docs\\mydocs.txt'), 'a') as f:
                f.write(f"{doc} \n")
        finally:
            print(f'Done appending {doc} to resources\\docs\\mydocs.txt')
        self.docLists.append(doc)
        docscount = len(self.docLists)
        # print(f'we now have {docscount} documents')
        count = 0

        with open(self.get_path('resources\\whatsAppUrls.txt'), 'r') as file:
            for line in file:
                if line == "\n":
                    print('\npassing blank line')
                    pass
                else:
                    count  += 1
                    if count <= 10:
                        with  open(self.get_path(f'resources\\docs\\WorkingDocs\\{doc}'), 'a') as d:
                            d.write(f"{line}\n")
                            self.deleteusedLink()
                            
                    else:
                        self.cleanlinks()
   
        # with open(self.get_path('resources\\whatsAppUrls.txt'), 'r') as file:
        #     for line in file:
        #         if line != "\n":
        #             count  += 1
        #             if count <= 10:
        #                 with  open(self.get_path(f'resources\\docs\\WorkingDocs\\{doc}'), 'a') as d:
        #                     d.write(f"{line}\n")
        #                     self.deleteusedLink()
                            
        #             else:
        #                 self.cleanlinks()


    def deleteusedLink(self):
        try:
            with open(self.get_path('resources\\whatsAppUrls.txt'), 'r') as fin:
                linkdata = fin.read().splitlines(True)
            with open(self.get_path('resources\\whatsAppUrls.txt'), 'w') as fout:
                
                fout.writelines(linkdata[1:])
                try:
                    link = linkdata[0]
                    if link == "":
                        print('\navoiding unnecessary spaces')
                        self.deleteusedLink()
                    if link == '\n':
                        print('avoiding unnecessary lines')
                        self.deleteusedLink()
                    return link
                    print(f'done deleting link {link}')
                except IndexError:
                    mess = "Hooray..... You are done You can exit the app now"
                    print(mess)
            
        finally:
            pass
    
    def get_path(self, filepath):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filepath)






if __name__ == '__main__':
    ed = FB_WhatsappLinksBot()
    sys.stdout.write("\n The bot is now starting...")
    ed.init()
