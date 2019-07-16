import os
import json
import FileHash as hasher
import time
import sys
import hashlib

Test = True

class FileHasher():
    def CalculateFileHash(target):
        ''' Returns a SHA1 hexidecimal hash of a file '''
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        with open(target, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()
    
    def Get(target):
        ''' Returns a SHA1 hexidecimal hash of a file '''
        return CalculateFileHash(target)

### Setup FileHasher module
hasher = FileHasher()


class IgnoreList():
    def __init__(self):
        self.list = self.GetIgnoreList()
    
    def GetIgnoreList(self):
        if os.path.exists('pysweep.ignore'):
            try:
                with open('pysweep.ignore', 'r') as ignorefile:
                    text = ignorefile.read()
                lines = text.split('\n')
                ignore_paths = []
                for each_line in lines:
                    if len(each_line) > 1 and each_line[0] != '#':
                        if ' ** ' in each_line:
                            line_pieces = each_line.split(' ** ')
                            if len(line_pieces) > 1:
                                ignore_paths.append(line_pieces)
                        else:
                            ignore_paths.append(each_line)
                return ignore_paths
            except:
                print 'Invalid pysweep.ignore file. No file paths will be ignored'
                raw_input('Press any key to continue. Ctrl+C to stop')

## Setup ignore.list
ignore = IgnoreList()


def DoNotIgnore(path):
    for each in ignore.list:
        if type(each) == str and path == each:
            return False
    
        else:    
            return True


def TargetFileList(target):
    file_paths_list = []
    target = os.path.abspath(target)

    for parent, directories, files in os.walk(target):
        for each_file in files:
            path = os.path.join(parent, each_file)
            file_paths_list.append(path)
    return file_paths_list

def TargetDirList(target):
    directory_paths_list = []
    target = os.path.abspath(target)
    for parent, directories, files in os.walk(target):
        for each_dir in directories:
            path = os.path.join(parent, each_dir)
            directory_paths_list.append(path)
    return directory_paths_list


def MasterList(master):
    json

def MakeMasterDirList(master):
    directory_paths_list = []
    #target = os.path.abspath(target) Do not set abs path for master list
    for parent, directories, files in os.walk(master):
        for each_dir in directories:
            path = os.path.join(parent, each_dir)

            directory_paths_list.append(path)
    return directory_paths_list

def MakeMasterFileList(master):
    file_paths_list = []
    #target = os.path.abspath(target) Do not set abs path for master list

    for parent, directories, files in os.walk(master):
        for each_file in files:
            path = os.path.join(parent, each_file)
            file_paths_list.append(path)
    return file_paths_list


def ReturnPathAs(string, operating_sys='Current'):
    restring = ''
    for each in string:
        if each == '/':
            restring += 'os_sep;'
        elif each == '\\':
            restring += 'os_sep;'
        #elif each == '\\':
        #    restring += 'os_sep;'
        else:
            restring += each
    listed = restring.split('os_sep;')

    os_path = os.path.join(*listed)
    if operating_sys == 'Windows':
        pass
    return os_path



def StringSnip(whole, snippet):
    ''' Returns the whole with the first instance of the snippet removed '''
    plength = len(snippet)
    i = 0
    new = ''
    pop = ''
    skip = None
    for each in whole:
        if whole[i:(i + plength)] == snippet:
            pop += each
            i += 1
            skip = 1
        elif skip != None and skip < plength:
            pop += each
            i += 1
            skip += 1
        else:
            new += each
            i += 1
    return new

def TestOnlyFunction():
    target = 'Target'
    master = 'Master/'

    t_dirs = TargetDirList(target)
    t_files = TargetFileList(target)

    m_dirs = MakeMasterDirList(master)
    m_files = MakeMasterFileList(master)

    #path = 'my/this/is/a/path'
    #pattern = ReturnPathAs('\\my\\this/')

    #pattern = os.path.join(pattern, '')

    #print StringSnip(path, pattern)

def CreateDirsList(master):
    target = master
    t_dirs = TargetDirList(target)
    dirlist = []
    for each in t_dirs:
        abs_path = each
        rel_path = StringSnip(abs_path, os.path.abspath(target))
        dirlist.append(rel_path)
    return dirlist


def CreateHashDict(master):
    target = master
    t_files = TargetFileList(target)
    dictionary = {}
    for each in t_files:
        abs_path = each
        rel_path = StringSnip(abs_path, os.path.abspath(target))
        dictionary[rel_path] =  hasher.Get(abs_path)
    #    t_abs = os.path.abspath(target)
    #    rel_path = StringSnip(each, t_abs)
    #    print rel_path
        #print abs_path

    return dictionary

def CreateMasterFile(master, filename):
    master = os.path.abspath(master)
    master_dirs = CreateDirsList(master)
    master_hash_dict = CreateHashDict(master)
    header = {
        'ROOT': master,
        'TYPE': 'master',
        'TIME': time.time()
        }
    data = {
        'HEADER': header,
        'DATA': {
            'FILES': master_hash_dict,
            'DIRS': master_dirs
            }
        }

    with open(filename, 'w') as output:
        json.dump(data, output, indent=4)

def CompareItemLists(list_one, list_two):
    missing_in_one = []
    missing_in_two = []
    for each in list_one:
        if each not in list_two and DoNotIgnore(each):
            missing_in_two.append(each)
    for each in list_two and DoNotIgnore(each):
        if each not in list_one:
            missing_in_one.append(each)

    return missing_in_one, missing_in_two


def GetMasterDirs(masterfile):
    with open(masterfile, 'r') as infile:
        data = json.load(infile)

    master_unicode = data['DATA']['DIRS']
    master_dirs = []
    for each in master_unicode:
        master_dirs.append(str(each))
    return master_dirs

def GetMasterHashDict(masterfile):
    with open(masterfile, 'r') as infile:
        data = json.load(infile)
    unicode_dict = data['DATA']['FILES']
    hash_dict = {}
    for each in unicode_dict:
        hash_dict[str(each)] = str(unicode_dict[each])
    return hash_dict

def GetMasterRoot(masterfile):
    with open(masterfile, 'r') as infile:
        data = json.load(infile)
        master_root = str(data['HEADER']['ROOT'])
        return master_root

def ReportBlock(title, content_list):
    text = '# # # %s # # #\n' % title
    if len(content_list) > 0:
        for each in content_list:
            #text += '# '
            text += each
            text += '\n'
    else:
        text += '-- None --\n'
    text += '# # # # # # # # # # # # # # # # #\n\n\n'
    return text

def CompareToMaster(masterfile, target):
    target = os.path.abspath(target)
    target_abs_path = target
    master_abs_path = GetMasterRoot(masterfile)
    target_dirs = CreateDirsList(target)
    master_dirs = GetMasterDirs(masterfile)

    xtr_dirs_target, mis_dirs_target = CompareItemLists(master_dirs, target_dirs)

    target_files = CreateHashDict(target)
    master_files = GetMasterHashDict(masterfile)
    compareable_files = []
    xtr_files_target, mis_files_target = [], []
    for each in target_files:
        if each in master_files:
            compareable_files.append(each)
        else:
            xtr_files_target.append(each)
    for each in master_files:
        if each in target_files:
            if each not in compareable_files:
                compareable_files.append(each)
        else:
            mis_files_target.append(each)


    hash_mismatch = []
    for each in compareable_files:
        master_hash = master_files[each]
        target_hash = target_files[each]

        if master_hash != target_hash:
            hash_mismatch.append(each)

    report_text = ''

    time_now = time.strftime('%Y-%m-%d %H:%M:%S')
    rpt_head = 'SCAN REPORT\n\n'
    rpt_head += 'Run Time: %s\n' % time_now
    rpt_head += 'Master File: %s\n' % masterfile
    rpt_head += 'Master Root: %s\n' % master_abs_path
    rpt_head += 'Target Root: %s\n\n\n' % target_abs_path


    report = ''
    report += rpt_head
    report += ReportBlock('EXTRA FILES IN TARGET', xtr_files_target)
    report += ReportBlock('FILE HASH MISMATCH', hash_mismatch)
    report += ReportBlock('EXTRA DIRECTORIES IN TARGET', xtr_dirs_target)
    report += ReportBlock('MISSING DIRECTORIES IN TARGET', mis_dirs_target)
    report += ReportBlock('MISSING FILES IN TARGET', mis_files_target)


    return report


def RunReport(master_json, target):
    '''Generate a report using a master.json created by CreateMasterFile('file.json').'''
    report_text = CompareToMaster(master_json, target)
    time_now = time.strftime('%Y-%m-%d_%H%M%S')
    report_name = 'Scan_Report_%s.txt' % time_now
    with open(report_name, 'w') as reportfile:
        reportfile.write(report_text)


# CreateMasterFile('files', 'fresnoclovisprayerbreakfast_master.json')
# RunReport('fresnoclovisprayerbreakfast_master.json', 'files')


def MainRun():
    commands = ['set-master', 'report', '-m', '-t']
    args = sys.argv[1:]
    if len(args) == 0:
        print 'No arguments provided.\nUsage: %s command -m /path/to/master.json -t /path/to/target/dir/' % __file__
        print 'Valid commands:', commands
        return
    
    if args[0] not in commands:
        print '"', args[0], '" invalid command.'
        print 'Usage: %s command -m /path/to/master.json -t /path/to/target/dir/' % __file__
        print 'Valid commands:', commands
        return

    cmd = args[0]
    if cmd == 'set-master' and '-m' in args and '-t' in args:
        m_ind = args.index('-m')
        t_ind = args.index('-t')
        try:
            master_file = args[m_ind + 1]
        except IndexError:
            print 'Invalid master file name'
            return

        try:
            master_dir = args[t_ind + 1]
        except IndexError:
            print 'Invalid master directory name'
            return

        CreateMasterFile(master_dir, master_file)

    if cmd == 'report' and '-m' in args and '-t' in args:
        m_ind = args.index('-m')
        t_ind = args.index('-t')
        usage_txt = 'Usage: %s report -m master.json -t path/to/target/directory'
        try:
            master_file = args[m_ind + 1]
        except IndexError:
            print 'Invalid master file name'
            print usage_txt
            return

        try:
            target_dir = args[t_ind + 1]
        except IndexError:
            print 'Invalid target directory name'
            print usage_txt
            return
        
        elif cmd == 'report' and 'help' in args:
            print usage_txt

        RunReport(master_file, target_dir)


if Test:
    print 'Running in Test mode. No MainRun() executed.'
    print 'Done'
elif __name__ == '__main__':
    MainRun()

    print 'Done'

