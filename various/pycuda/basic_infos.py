import pycuda.driver as drv
drv.init()
for i in range(drv.Device.count()):
    cc_cores_per_SM_dict = {
    (2,0) : 32,
    (2,1) : 48,
    (3,0) : 192,
    (3,5) : 192,
    (3,7) : 192,
    (5,0) : 128,
    (5,2) : 128,
    (6,0) : 64,
    (6,1) : 128,
    (7,0) : 64,
    (7,5) : 64,
    (8,0) : 64,
    (8,6) : 128
    }
    gpu_device = drv.Device(i)
    print "Device {}: {}".format(i, gpu_device.name())
    compute_capability = float('%d.%d' %gpu_device.compute_capability()) 
    my_cc  = gpu_device.compute_capability()
    my_sms = gpu_device.multiprocessor_count
    
    print "\t  Compute Capability: {}".format(compute_capability)
    print "\t  Total Memory: {} megabytes".format(gpu_device.total_memory()//1024.0**2)
    print "\t  total number of SMs: {} ".format(gpu_device.multiprocessor_count)
    cores_per_sm = cc_cores_per_SM_dict.get(my_cc)
    total_cores = cores_per_sm*my_sms
    print "\t  total cuda cores per SM: {} ".format(cores_per_sm)
    print "\t  total cuda cores: {} ".format(total_cores)
    
