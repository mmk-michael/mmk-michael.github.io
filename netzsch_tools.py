def read_netzsch_expdat_file(file):
    import json # For making string into dict

    meta = {}
    columns = []
    data = []
    
    with open(file) as f:
        for line in f.readlines():
            if line.startswith("#") and not line.startswith('##'):
                d = line.strip('#\n').split(':') # make a dict of the line
                meta |= {d[0]: d[1]} # combine the dict into the main output meta-data dict 
            elif line.startswith("##"):
                columns = line.strip('#\n').split(';')
            elif not line.startswith('\n'):
                data.append(line.strip('\n').split(';'))
        
    meta = format_segment_keys(meta) # Split the segments into individual sections
    return meta, columns, data

def format_segment_keys(meta):
    for k in list(meta):
        if "SEG." in meta[k]:
            segment_labels = ['Initial T', 'Rate/Duration', 'Target T']
            segment_values = [meta[k].split('/',1)[0], meta[k].split('/')[1].rsplit('/',1)[0], meta[k].split('/')[1].rsplit('/',1)[1]]
            segment = dict(zip(segment_labels, segment_values))
            meta[k] = segment

            I = int(meta[k]['Initial T'][:-2]) # Strips °C 
            R = meta[k]['Rate/Duration']
            T = int(meta[k]['Target T'][:-2])
            if T > I:
                segment['Type'] = 'Heating'
            elif T < I:
                segment['Type'] = 'Cooling'
            elif T == I:
                segment['Type'] = 'Isothermal'
    return meta


# class NetzschExpDatFile(file):
#     def __init__(self):
#         self.metameta = {}
#         self.columns = []
#         self.data = []
