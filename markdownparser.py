import os
def getlist_input_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines

def markdown_parser(file_name):
    input_file_list = getlist_input_file(file_name)
    
    #flag to check that if praragraph is open or not   
    open_para_flag = 0

    #flag to check that if list is started not 
    bullet_list_flag=0
    
    for line in range(len(input_file_list)):
        #heading
        if(input_file_list[line].lstrip(' ').startswith('#')):
            i = 1
            while((input_file_list[line][i] == '#') and i < len(input_file_list[line])):
                i+=1
            hash_count = i
            input_file_list[line] = "<h" + str(hash_count) + ">" + input_file_list[line][:-1].replace("#","",hash_count) + " </h" + str(hash_count) + ">" + "\n"
        
        #blank lines
        elif(input_file_list[line].lstrip(' ').startswith('\n')):
            if(open_para_flag == 0):
                input_file_list[line] = input_file_list[line].replace('\n','<p>',1)
                open_para_flag = 1
            elif(open_para_flag == 1):
                input_file_list[line] = input_file_list[line].replace('\n','</p><p>',1)              
            else:
                input_file_list[line] = input_file_list[line].replace('\n','</p>',1)
        
        #line break
        if(input_file_list[line][0:-1].endswith('  ')):
           input_file_list[line] = input_file_list[line][0:-3] + "<br/>"   
           
        #bullet list                      
        if(input_file_list[line].lstrip().startswith('* ')):
            if bullet_list_flag==0:
                input_file_list[line]='<ul>\n<li>'+input_file_list[line].replace('*',"",1)+'</li>'
                if(input_file_list[line+1].lstrip().startswith('* ')):
                    bullet_list_flag=1
                else:
                    bullet_list_flag=0
                    input_file_list[line]=input_file_list[line]+'</ul>'

            else:
                input_file_list[line]='<li>'+input_file_list[line].replace('*',"",1)+'</li>'
                if(input_file_list[line+1].lstrip().startswith('* ')):
                    bullet_list_flag=1
                else:
                    bullet_list_flag=0
                    input_file_list[line]=input_file_list[line]+'</ul>'
        
          
        #bold 
        loop_star_counter = (input_file_list[line].count('**') )
        result_string=''

        if(loop_star_counter>1):
            temp_list=input_file_list[line].split()
            for i in temp_list:
                if(i.startswith('**') and i.endswith('**') and len(i)>4):
                    result_string+='<strong>'+i.replace('**','',2)+'</strong> '
                else:
                    result_string+=i+" "
            input_file_list[line]=result_string
        
        #italic
        loop_underscore_counter = (input_file_list[line].count('_') )
        result_string=''

        if(loop_underscore_counter>1):
            temp_list=input_file_list[line].split()
            for i in temp_list:
                if(i.startswith('_') and i.endswith('_') and len(i)>2):
                    result_string+='<em>'+i.replace('_','',2)+'</em> '
                else:
                    result_string+=i+' '
            input_file_list[line]=result_string

    #closing the para in last if open
    if open_para_flag ==1:
        input_file_list.append('</p>')

    # writing the result to created html file 
    output=''.join(input_file_list)
    with open('sample.html','w') as f:
        f.write(output)
    
                 
#calling markdown_parser() which take the input from 'sample.md' and convert it to corressponding html tags and write it into 'sample.html'
markdown_parser('sample.md')
