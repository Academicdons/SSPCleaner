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
        self.docNumber = 0
        self.cleanlinks()

    def cleanlinks(self):
        if self.countLinks() == 0:
            with open(self.get_path('resources\\docs\\mydocs.txt'), 'a') as f:
                f.write('No Links collected')
            print('Done manupilating links in', "--- %s seconds ---" % (time.time() - self.start_time))
            raise SystemExit(0)

        self.docLists = []
        self.docNumber += 1
        doc = f'linkDoc{self.docNumber}.txt'
        try:
            with open(self.get_path('resources\\docs\\mydocs.txt'), 'a') as f:
                f.write(f"{doc} \n") # writes down the list of document
        finally:
            print(f'Done appending {doc} to resources\\docs\\mydocs.txt')
        self.docLists.append(doc)
        docscount = len(self.docLists)
        # print(f'we now have {docscount} documents')
        count = 0
        with open(self.get_path('resources\\whatsAppUrls.txt'), 'r') as file:
            with  open(self.get_path(f'resources\\docs\\WorkingDocs\\{doc}'), 'a') as d:
                for line in file:
                    if line == "\n":
                        print('\npassing blank line')
                        pass
                    else:
                        print(f'\nAdding link: {line}')
                        count  += 1
                        if count <= 5:
                            d.write(f"{line}\n")
                            lineToDelete = line
                            self.deleteusedLink(lineToDelete)
                        else:
                            print('count is more than 5 going back to start new file')
                            self.cleanlinks()
   

    def deleteusedLink(self, lineToDelete):
        try:
            file = self.get_path('resources\\whatsAppUrls.txt')
            with open(file, 'r+') as f: # open file in read / write mode
                firstLine = f.readline() # read the first line and throw it out
                data = f.read() # read the rest
                f.seek(0) # set the cursor to the top of the file
                f.write(data) # write the data back
                f.truncate() # set the file size to the current size
                return firstLine
           
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
