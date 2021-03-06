import os
import sys
import time

def check_exists(a):
    if not os.path.exists(a):
        sys.exit('File not exists:%s'%a)

def single_run_euroc(orb_dir, data_dir, ts_file, out_file):
    print('Run EuRoC data: %s'%data_dir)
    t1 = time.time()
    exe = os.path.join(orb_dir,'build/demo_stereo_euroc')
    param = os.path.join(orb_dir,'param/euroc_stereo_imu.yaml')
    left_imgdir = os.path.join(data_dir,'mav0/cam0/data')
    right_imgdir = os.path.join(data_dir,'mav0/cam1/data')
    cmd_list = (exe,param,ts_file,left_imgdir,right_imgdir)
    for f in cmd_list:
        if not os.path.exists(f):
            sys.exit('File not exists:%s'%f)

    os.system('%s %s %s %s %s'%cmd_list)
    time.sleep(10)
    os.system('mv vio.txt %s'%out_file)
    print('Done. %.2f Seconds.'%(time.time()-t1))

def batch_run_euroc(orb_dir, whole_dir, res_dir, select_dataset = None):
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    if select_dataset is None:
        select_dataset = [x for x in os.listdir(whole_dir) if os.path.exists(os.path.join(whole_dir,x,'mav0'))]

    for name in select_dataset:
        path = os.path.join(whole_dir, name)
        ts_file = os.path.join(sys.path[0],'euroc_stamp','%s.txt'%name)
        out_file = os.path.join(res_dir, 'out_%s.txt'%name)
        single_run_euroc(orb_dir, path, ts_file, out_file)

if __name__ == '__main__':
    svo_dir = '/home/symao/workspace/svo2_noros/'
    whole_dir = '/home/symao/data/euroc/zip'
    res_dir = './results'
    # data_list = ['MH_01_easy', 'MH_02_easy', 'MH_03_medium', 'MH_04_difficult', 'MH_05_difficult',
    #          'V1_01_easy', 'V1_02_medium', 'V1_03_difficult',
    #          'V2_01_easy', 'V2_02_medium', 'V2_03_difficult']
    batch_run_euroc(svo_dir, whole_dir, res_dir)
