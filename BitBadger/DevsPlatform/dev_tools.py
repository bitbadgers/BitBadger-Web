import os
class MinifyFile():
    def __init__(self,file):
        self.file_name = str(file)
        self.file = file
        self.handle_uploaded_file(file)
        self.FileReader()
        
    def FileReader(self):
        with open('kk.js') as file_object:
            self.lines = file_object.readlines()
            os.remove('kk.js')

    def RemoveDoubleSlashComment(self):

        double_slash_commentless_list = [] #stores the code with no halfline cpmments
        for line in self.lines:
            test = str(line).split("//")
            double_slash_commentless_list.append(test[0])
                
        return double_slash_commentless_list
    
    def CommentLessCombine(self):#converts the code from a list to string
        code_list = self.RemoveDoubleSlashComment()
        new_code_string = ''
        for line in code_list:
            new_code_string+=str(line)
            
        return new_code_string
    
    def Replacer(self):
        code_string = str(self.CommentLessCombine())
        one_line_code = code_string.replace('\n',";").replace('\t'," ").replace('    ',' ').replace('   ',' ').replace('  ',
        ' ').replace('/ ','/').replace(' /','/').replace('; ',';').replace(';;',';').replace('; ;',
        ';').replace('};','}').replace('{;','{').replace("} ;",'}').replace("/;",
        "/").replace(';;',';').replace('( ','(').replace('{ ','{').replace('[ ',
        '[').replace(' = ','=').replace('= ','=').replace(' =','=').replace('( ',
        '(').replace(' )',')').replace(') ',')').replace(' (','(').replace(' {','{').replace('{ ',
        '{').replace(' {','{').replace(' }','}').replace('} ','}').replace(' + ',
        '+').replace(' +','+').replace(' +','+').replace(' - ','-').replace(' -','-').replace('- ','-')
        
        return one_line_code
    
    def RemoveComments(self): #remove the /**/ comment
        text = str(self.Replacer())
        code_length = len(text)
        index = 0
        replacing_text_list = []
        while(index < code_length):
            if text[index] == '/':
                if(index +1 ) < code_length:
                    if text[index+1] == '*':
                        y = ''
                        index += 2 
                        while((text[index] + text[index+1]) != '*/'):
                            y += text[index]
                            index += 1
                        replacing_text = '/*'+y+'*/'
                        replacing_text_list.append(replacing_text)
                        
            index+=1
            
        new_commentless_string = text
        for item in replacing_text_list:
            new_commentless_string = new_commentless_string.replace(str(item), '')
            
        return new_commentless_string
            
    def RemoveIrrelevantSpaces(self):
        string = str(self.RemoveComments())
        length = len(string)
        index = 0
        replaced = []
        replacer = []
        while(index < length):
            if string[index] == '[':
                index += 1
                replacerIndex = len(replacer) - 1
                y = ''
                while(string[index] != ']'):
                    y += string[index]
                    # replacer[replacerIndex].append(string[index])
                    index +=1
                replaced.append(y)
                replacer.append(y.replace(', ',',').replace(' ,',',').replace(' , ',','))
            index += 1
        
        index = 0
        new_string = string
        for item in replaced:
            new_string = new_string.replace(replaced[index],replacer[index])
            index += 1
            
        return new_string
    
    def GenerateNewFileName(self):
        name = self.file_name.split('.')
        last_index = len(name)-1
        file_extension = name[last_index]
        minified_file_name = self.file_name.replace(file_extension, 'min.'+file_extension)
        return minified_file_name
    
    def Minify(self):
        path = ""
        filename = self.GenerateNewFileName()
        full_file_name = path+filename
        
        with open(full_file_name, 'w') as file_object:
            file_object.write(self.RemoveIrrelevantSpaces().lstrip('b'))
            
        return {
            'file_path' : path,
            'filename' : filename
        }
        
    def handle_uploaded_file(self, file):
        with open("kk.js", 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)