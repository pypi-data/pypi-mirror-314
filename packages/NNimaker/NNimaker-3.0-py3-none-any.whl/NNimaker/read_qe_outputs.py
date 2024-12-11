from collections import deque, Counter
import json
import glob
import argparse
import os

def tot_string(s):
    return s.split('CPU')[-1].replace('WALL', '').strip().replace(' ', '')

def is_qe_output_file(filepath):
    """Check if a file is a Quantum ESPRESSO output by inspecting its start and end content."""
    try:
        with open(filepath, 'r') as file:
            # Check the first few lines for the start marker
            for _ in range(10):
                line = file.readline()
                if "Program PWSCF" in line:
                    break
            else:
                return False  # If the loop finishes without finding the marker

        # Now check the end of the file for the termination marker "JOB DONE"
        with open(filepath, 'rb') as file:
            file.seek(0, os.SEEK_END)
            position = file.tell()

            # Define a reasonable number of lines to check from the end
            lines_to_check = 50
            buffer_size = 1024  # Read in chunks of 1KB
            lines = []
            while position > 0 and lines_to_check > 0:
                position -= buffer_size
                if position < 0:
                    position = 0
                file.seek(position)
                chunk = file.read(buffer_size)

                # Break the chunk into lines and prepend them to the list
                lines = chunk.splitlines() + lines

                # Count the lines from the end
                lines_to_check -= len(lines)

                # If we've read enough lines, stop
                if lines_to_check <= 0:
                    break

            # Check the last few lines for the "JOB DONE" marker
            for line in reversed(lines):
                if b"JOB DONE" in line:
                    return True

    except (UnicodeDecodeError, OSError):
        return False

    return False

# some of QE files missing the phrase:'Q(r) pseudized with'
#def read_betas(fname):
 #   with open(fname, 'r') as f:
  #      l_ = f.readlines()
   # index_start = [i+1 for i,
    #               _ in enumerate(l_) if 'Using radial grid of ' in _]
   # index_end = [i for i, _ in enumerate(l_) if 'Q(r) pseudized with' in _]
   # all_orbs = ''
   # nbetas = ''
   # for s, e in zip(index_start, index_end):
   #     nbeta = "|%s|" % (l_[s-1].split()[6])
   #     orbs = ["|%s|" % (_.split()[2]) for _ in l_[s:e]]
   #     all_orbs += "".join(orbs)
   #     nbetas += nbeta
   # return nbetas, all_orbs
    
def read_betas(fname):
    with open(fname, 'r') as f:
        l_ = f.readlines()

    # Identify the indices for beta sections
    index_start = [i + 1 for i, line in enumerate(l_) if 'Using radial grid of ' in line]
    index_end = []
    
    # Dynamically determine the end markers for each block
    for start_idx in index_start:
        # Look for the next 'Q(r) pseudized with' or next 'PseudoPot.' as a fallback
        end_idx = next(
            (i for i in range(start_idx, len(l_))
             if 'Q(r) pseudized with' in l_[i] or 'PseudoPot.' in l_[i]),
            len(l_)  # Default to end of file if no end marker is found
        )
        index_end.append(end_idx)

    nbetas = ""
    all_orbs = ""

    for s, e in zip(index_start, index_end):
        try:
            # Extract beta and orbital information safely
            nbeta = "|%s|" % (l_[s - 1].split()[6])
            orbs = [
                "|%s|" % (_.split()[2])
                for _ in l_[s:e]
                if len(_.split()) > 2  # Ensure the line has enough tokens
            ]
            all_orbs += "".join(orbs)
            nbetas += nbeta
        except IndexError as err:
            print(f"IndexError in file {fname} between lines {s} and {e}: {err}")
            print(f"Skipping problematic section.")
            continue
        except Exception as err:
            print(f"Unexpected error in file {fname} between lines {s} and {e}: {err}")
            raise

    return nbetas, all_orbs



def read_additional_info(fname):
    with open(fname, 'r') as f:
        l_ = f.readlines()
    natoms = [_.split()[-1] for _ in l_ if 'number of atoms/cell' in _][0]
    species = [_.split()[1] for _ in l_ if 'tau(' in _]
    species = species[:int(natoms)]
    n_spec = dict(Counter(species))
    species_line = ["|%s||%i|" % (k, v) for k, v in n_spec.items()]
    species_line = "".join(species_line)
    psuedo_line = ["|%s|" % (k) for k in n_spec.keys()]
    psuedo_line = "".join(psuedo_line)
    nel = [_.split()[-1] for _ in l_ if 'number of electrons' in _][0]
    conv_thresh = [_.split()[-1]
                   for _ in l_ if 'convergence threshold' in _][0]
    n_g_smooth = [_.split()[2] for _ in l_ if 'Smooth grid:' in _][0]
    n_g_dense = [_.split()[2] for _ in l_ if 'Dense  grid:' in _][0]
    return (nel, species_line, len(n_spec),
            n_g_smooth, n_g_dense, conv_thresh, psuedo_line)


def read_tot(s):
    t = s.partition('s')[0]
    part = t.partition('m')
    if part[1] == 'm':
        try:
            res = float(part[2])
        except ValueError:
            res = 0.
        t = part[0]
        part = t.partition('h')
        if part[1] == 'h':
            res = res + 60*(float(part[2])+60*float(part[0]))
        else:
            res = res+60*float(part[0])
    else:
        res = float(part[0])
    return res


def read_clocks(filename):
    with open(filename, 'r') as f:
        clocklines = deque(filter(lambda s: ' CPU ' in s and ' WALL' in s, f))
    if len(clocklines) == 0:
        return None
    for prog in ['PWSCF', 'CP ']:
        totclock = deque(filter(lambda s: prog in s, clocklines), maxlen=1)
        if len(totclock) == 1:
            # res = ((prog, read_tot(totclock[0].split()[-2])),)
            res = ((prog, read_tot(tot_string(totclock[0]))),)
            break
    clocks = [
        (_.split()[0], float(_.split()[4].replace('s', '')))
        for _ in clocklines
        if ('PWSCF' not in _) and ('CP ' not in _)]
    return tuple(clocks)+res


def read_iterations(filename):
    with open(filename, 'r') as f:
        clocklines = [_ for _ in f.readlines(
        ) if ' CPU ' in _ and ' WALL' in _]
    iterations = [
        (_.split()[0], float(_.split()[7].replace('s', '')))
        for _ in clocklines
        if ('PWSCF' not in _) and ('CP ' not in _)]
    return tuple(iterations)


def read_program(filename):
    with open(filename) as f:
        startline = [_ for _ in f.readlines(
        ) if 'Program' in _ and 'starts' in _][0]
    return startline.split()[1]


def read_ndiag(line):
    ll = line.split('*')[1]
    ndiag = int(ll.split()[0])
    return ndiag*ndiag


def read_parallel(filename):
    with open(filename, 'r') as f:
        l_ = f.readlines()[:50]
    try:
        linetoread = [_ for _ in l_ if 'Number of MPI processes:' in _][0]
    except IndexError:
        return None
    res = {'MPI tasks': int(linetoread.split()[4])}
    linetoread = [_ for _ in l_ if 'Threads/MPI process:' in _][0]
    res.update({'Threads': int(linetoread.split()[2])})
    try:
        linetoread = [_ for _ in l_ if "K-points division:     npool" in _][0]
        res.update({'npool': int(linetoread.split()[-1])})
    except IndexError:
        res.update({'npool': 1})
    try:
        linetoread = [_ for _ in l_ if "R & G space division:" in _][0]
        r_n_g = int(linetoread.split()[-1])
        res.update({'n_RG': r_n_g})
    except IndexError:
        r_n_g = 1
    linetoread = [_ for _ in l_ if "wavefunctions fft division:" in _]
    if len(linetoread) == 0:
        wfc_fftdiv = (1, r_n_g)
    elif len(linetoread) > 0:
        wfc_fftdiv = tuple([int(_) for _ in (linetoread[0]).split()[-2:]])
    res.update({"wfc_fft_division": wfc_fftdiv})
    res.update({"taskgroups": len(linetoread) == 2})
    try:
        linetoread = [_ for _ in l_ if "distributed-memory algorithm" in _][0]
        res.update({'ndiag': read_ndiag(linetoread)})
    except IndexError:
        res.update({'ndiag': 1})
    return res


def read_gridinfo(filename, stringa):
    """
    filename: str path of the file to open
    stringa:  str string to search for selecting the line
    """
    with open(filename, 'r') as f:
        r = deque(filter(lambda _: stringa in _, iter(f)))[0]
    temp1, temp2 = r.split(":")[1], r.split(":")[2]
    grid_vecs = int(temp1.split()[0])
    temp2 = temp2.replace('(', ' ').replace(')', ' ').replace(',', ' ')
    fft_dims = tuple((int(_) for _ in temp2.split()))
    return {"ngrid_vecs": grid_vecs, "fft_dims": fft_dims}


def read_dimensions(filename):
    with open(filename, 'r') as f:
        l_ = f.readlines()
    s = "number of atoms/cell"
    try:
        r = [_ for _ in l_ if s in _][0]
    except IndexError:
        return None
    res = {'nat': int(r.split()[-1])}
    s = "number of Kohn-Sham states="
    try:
        r = [_ for _ in l_ if s in _][0]
    except IndexError:
        return None
    res.update({'nbands': int(r.split()[-1])})
    s = "kinetic-energy cutoff"
    r = [_ for _ in l_ if s in _][0]
    res.update({'ecutwfc': float(r.split()[-2])})
    s = "charge density cutoff"
    r = [_ for _ in l_ if s in _][0]
    res.update({'ecutrho': float(r.split()[-2])})
    s = "unit-cell volume"
    r = [_ for _ in l_ if s in _][0]
    res.update({'vol': float(r.split()[-2])})
    dense_fft_dims = read_gridinfo(filename, "Dense  grid:")
    smooth_fft_dims = read_gridinfo(filename, "Smooth grid:")
    res.update({"Dense_grid": dense_fft_dims, "Smooth_grid": smooth_fft_dims})
    with open(filename, 'r') as f:
        r = deque(filter(lambda _: "Smooth grid:" in _, iter(f)))[0]
    return res


def read_raminfo(filename):
    total_ram = read_estimated_ram(filename)
    if total_ram is None:
        return None
    res = total_ram
    partial_ram = read_partial_ram(filename)
    if partial_ram is not None:
        res.update(partial_ram)
    return res


def read_estimated_ram(filename):
    with open(filename, 'r') as f:
        lines = [_ for _ in filter(
            lambda _: "Estimated" in _ and "RAM" in _, iter(f))]
    if len(lines) < 3:
        return None
    temp = lines[0].split('>')[1].split()
    static = (float(temp[0]), temp[1])
    temp = lines[1].split('>')[1].split()
    max_dynamic = (float(temp[0]), temp[1])
    temp = lines[2].split('>')[1].split()
    total = (float(temp[0]), temp[1])
    return {
        "static_per_process": static,
        "max_per_process": max_dynamic,
        "total": total
    }


def read_partial_ram(filename):
    with open(filename, 'r') as f:
        lines = [_ for _ in filter(lambda _:"Dynamical RAM for" in _, iter(f))]
    if len(lines) == 0:
        return None

    def read_line(_):
        temp1, temp2 = _.split(":")
        temp1 = temp1.replace("Dynamical RAM for", "").strip()
        return temp1, float(temp2.split()[0]), temp2.split()[1]
    itera = ((read_line(l)[0], read_line(l)[1:]) for l in lines)
    return dict(tuple(itera))


def read_nkpoints(fname):
    with open(fname, 'r') as fr:
        l_ = filter(lambda s: 'number of k points' in s, fr)
        l_ = deque(l_, maxlen=1)
    if len(l_) == 1:
        return int(l_[0].split()[4])
    else:
        return None


def get(fname, algoname='davidson', other_info=None):
    dims = read_dimensions(fname)
    if dims is None:
        # print("No dims for this file", fname)
        return None
    nk = read_nkpoints(fname)
    if nk is None:
        print("No k points for this file", fname)
        return None
    dims.update({'nkpoints': nk})
    para = read_parallel(fname)
    try:
        clocks = dict(read_clocks(fname))
        iterations = dict(read_iterations(fname))
    except TypeError:
        print("No Clock for this file", fname)
        return None
    raminfo = read_raminfo(fname)
    data1 = {"output": fname, 'algo': algoname}
    data1.update({'clocks': clocks})
    data1.update({'iter': iterations})
    dims.update(para)
    data1.update({'dims': dims})

    (nel, species_line, n_species, n_g_smooth,
     n_g_dense, conv_thresh, pseudo) = read_additional_info(
        fname)
    nbetas, all_orbs = read_betas(fname)
    data1.update({'Nbeta': nbetas})
    data1.update({'Nl': all_orbs})
    data1.update({'n_el': nel})
    data1.update({'n_species': n_species})
    data1.update({'NatomsType': species_line})
    data1.update({'pseudo': pseudo})
    data1.update({'smooth_grid_rec': n_g_smooth})
    data1.update({'dense_grid_rec': n_g_dense})
    data1.update({'convergence': conv_thresh})

    if other_info is not None:
        data1.update(other_info)
    if raminfo is not None:
        data1.update({"RAM": raminfo})
    return data1

#_____________This function is for adding identikeep info to NN input. 

def extract_other_info(sysinfo_path, platform='Leonardo-booster'):
    """Extracts relevant hardware information from sysinfo.json."""
    with open(sysinfo_path, 'r') as file:
        sysinfo = json.load(file)

    # Initialize variables to collect information
    cpu_models = set()
    gpu_count = 0
    gpu_devices =set()
    total_memory_kb = 0
    node_count = len(sysinfo.get('NodeList', []))
    # Iterate through nodes and processes to gather information
    for node in sysinfo.get('NodeList', []):

        for proc in node.get('ProcList', []):
   
            cpu_info = proc.get('CPU', {})
            # Collect CPU models (unique entries)
            cpu_models.update(cpu_info.get('cpuModel', {}).get('value', []))
            
            # Extract memory information
            if proc.get('GlobalRank') == 0:
                mem_info = proc.get('MEM', {})
                mem_total_list = mem_info.get('memTotal', {}).get('value', [])
                if mem_total_list:  # Check if the list is not empty
                    total_memory_kb += mem_total_list[0]  # Add the first element of the list
                gpu_info = proc.get('CUDA', {})
                gpu_count = len(gpu_info.get('cudaDevice', {}).get('value', []))
                gpu_devices.update(gpu_info.get('cudaDevice', {}).get('value', []))
    # Convert total memory from kilobytes to gigabytes
    total_memory_gb = total_memory_kb / (1024 * 1024)  # Convert KB to GB

    # Use the first CPU model found or a default value if none found
    cpu_model = next(iter(cpu_models), "Unknown CPU Model")
    #node_info = f"{node_count}*{cpu_model}"
    
    gpu_device = next(iter(gpu_devices), "Unknown GPU Device")
    node_info = f"{node_count}*{cpu_model}, GPU:{gpu_count}*{gpu_device}"
    other_info = {
        "Platform": platform,
        "CPU": cpu_model,
        "Node": node_info,
        "Memory": f"{total_memory_gb:.2f} GB DDR4 RAM"
    }

    return other_info
#_______________________________________________________________

def create_json(folder="./", outname="data.json", platform='Leonardo-booster', algoname='davidson'):
    # Load other_info from 'sysinfo.json' in the folder
    sysinfo_path = os.path.join(folder, 'sysinfo.json')
    
    # Check if 'sysinfo.json' exists
    if os.path.isfile(sysinfo_path):
        other_info = extract_other_info(sysinfo_path, platform) 
    else:
        other_info = {"Platform": platform }
   
####0.V
    # Automatically recognize input files in the directory
    #pathre = os.path.join(folder, '*')  # Match all files except 'sysinfo.json'
####0.V    

    # Automatically recognize QE output files by inspecting content
    qe_files = [f for f in glob.glob(os.path.join(folder, '*')) if is_qe_output_file(f)]
    
    if not qe_files:
        print(f"Error: No complete QE output files found in the specified directory: {folder}")
        print("Please ensure that the required QE output files are present and properly terminated.")
        return
    
    
    data = (get(n, algoname=algoname, other_info=other_info) for n in qe_files if os.path.isfile(n))
    data = [_ for _ in filter(None, data)]

    with open(outname, 'w') as fw:
        json.dump(data, fw, indent=2)
    
    print(f"Data successfully saved to {outname}")

####  0.V        
    # data = (get(n, algoname=algoname, other_info=other_info) for n in glob.glob(pathre) if os.path.isfile(n) and os.path.basename(n) != 'sysinfo.json')
    # data = [_ for _ in filter(None, data)]

    # Save the aggregated data to the output JSON file
    # with open(outname, 'w') as fw:
    #   json.dump(data, fw, indent=2)
#### 0.V 
    return data
    

def nnimake_qe():
    parser = argparse.ArgumentParser(description="Create a JSON file by processing all files in a directory.")
    parser.add_argument('--folder', type=str, default='./', help='The directory containing input files  (default: ./ )')
    parser.add_argument('--outname', type=str, default='data.json', help='Output JSON filename (default: data.json)')
    parser.add_argument('--platform', type=str, default='Leonardo-booster', help='Name of supercomputer or platform you have used (default: Leonardo-booster)')
    parser.add_argument('--algoname', type=str, default='davidson', help='Algorithm name to be used (default: davidson)')

    args = parser.parse_args()

    create_json(args.folder, outname=args.outname, platform=args.platform, algoname=args.algoname)

if __name__ == "__main__":
    nnimake_qe()

