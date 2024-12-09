"""
SatNOGS Decoder subpackage initialization
"""
from __future__ import absolute_import, division, print_function

import enum
import functools
import re

from .aausat4 import Aausat4
from .acrux1 import Acrux1
from .aepex import Aepex
from .alsat1n import Alsat1n
from .amicalsat import Amicalsat
from .armadillo import Armadillo
from .ascii85test import Ascii85test
from .astrocast import Astrocast
from .asuphoenix import Asuphoenix
from .ax25frames import Ax25frames
from .ax25monitor import Ax25monitor
from .azaadisat2 import Azaadisat2
from .bdsat import Bdsat
from .bdsat2 import Bdsat2
from .beesat import Beesat
from .beesat2 import Beesat2
from .bisonsat import Bisonsat
from .bobcat1 import Bobcat1
from .bugsat1 import Bugsat1
from .cape1 import Cape1
from .cas4 import Cas4
from .cas5a import Cas5a
from .cas9 import Cas9
from .catsat import Catsat
from .celesta import Celesta
from .chomptt import Chomptt
from .cirbe import Cirbe
from .co65 import Co65
from .connectat11 import Connectat11
from .cosmogirlsat import Cosmogirlsat
from .crocube import Crocube
from .csim import Csim
from .ctim import Ctim
from .cubebel1 import Cubebel1
from .cubebel2 import Cubebel2
from .cubesatsim import Cubesatsim
from .cute import Cute
from .delfin3xt import Delfin3xt
from .delfipq import Delfipq
from .dhabisat import Dhabisat
from .diy1 import Diy1
from .dora import Dora
from .duchifat3 import Duchifat3
from .eirsat1 import Eirsat1
from .elfin import Elfin
from .enso import Enso
from .entrysat import Entrysat
from .equisat import Equisat
from .eshail2 import Eshail2
from .estcube2 import Estcube2
from .foresail1 import Foresail1
from .fox import Fox
from .gaspacs import Gaspacs
from .geoscan import Geoscan
from .geoscanedelveis import Geoscanedelveis
from .grbalpha import Grbalpha
from .grbbeta import Grbbeta
from .greencube import Greencube
from .grizu263a import Grizu263a
from .gt1 import Gt1
from .hadesd import Hadesd
from .inspiresat1 import Inspiresat1
from .io86 import Io86
from .irazu import Irazu
from .irvine import Irvine
from .iss import Iss
from .kafasat1 import Kafasat1
from .kashiwa import Kashiwa
from .kosen1 import Kosen1
from .ksu import Ksu
from .ledsat import Ledsat
from .lightsail2 import Lightsail2
from .lucky7 import Lucky7
from .meznsat import Meznsat
from .minxss import Minxss
from .mirsat1 import Mirsat1
from .mitee1 import Mitee1
from .mxl import Mxl
from .mysat import Mysat
from .netsat import Netsat
from .neudose import Neudose
from .neutron1 import Neutron1
from .no44 import No44
from .nutsat1 import Nutsat1
from .opssat1 import Opssat1
from .oresat0 import Oresat0
from .oresat0_5 import Oresat05
from .origamisat1 import Origamisat1
from .painani import Painani
from .pegasus import Pegasus
from .picsat import Picsat
from .planetum1 import Planetum1
from .polyitan1 import Polyitan1
from .pwsat2 import Pwsat2
from .qarman import Qarman
from .qbee import Qbee
from .qube import Qube
from .qubik import Qubik
from .quetzal1 import Quetzal1
from .ramsat import Ramsat
from .randev import Randev
from .rhoksat import Rhoksat
from .roseycubesat1 import Roseycubesat1
from .sakura import Sakura
from .salsat import Salsat
from .sanosat1 import Sanosat1
from .selfiesat import Selfiesat
from .sharjahsat1 import Sharjahsat1
from .siriussat import Siriussat
from .skcube import Skcube
from .snet import Snet
from .spoc import Spoc
from .sputnixusp import Sputnixusp
from .sr0 import Sr0
from .strand import Strand
from .stratosattk1 import Stratosattk1
from .suchai2 import Suchai2
from .targit import Targit
from .us6 import Us6
from .uwe4 import Uwe4
from .veronika import Veronika
from .vzlusat2 import Vzlusat2
from .yomogi import Yomogi

__all__ = [
    'Aausat4',
    'Acrux1',
    'Aepex',
    'Alsat1n',
    'Amicalsat',
    'Armadillo',
    'Ascii85test',
    'Astrocast',
    'Asuphoenix',
    'Ax25frames',
    'Ax25monitor',
    'Azaadisat2',
    'Bdsat',
    'Bdsat2',
    'Beesat',
    'Beesat2',
    'Bisonsat',
    'Bobcat1',
    'Bugsat1',
    'Cape1',
    'Cas4',
    'Cas5a',
    'Cas9',
    'Catsat',
    'Celesta',
    'Chomptt',
    'Co65',
    'Connectat11',
    'Cosmogirlsat',
    'Crocube',
    'Cubebel1',
    'Cubebel2',
    'Cubesatsim',
    'Cute',
    'Csim',
    'Ctim',
    'Cirbe',
    'Delfin3xt',
    'Delfipq',
    'Dhabisat',
    'Diy1',
    'Dora',
    'Duchifat3',
    'Eirsat1',
    'Elfin',
    'Enso',
    'Entrysat',
    'Eshail2',
    'Equisat',
    'Estcube2',
    'Foresail1',
    'Fox',
    'Gaspacs',
    'Geoscan',
    'Geoscanedelveis',
    'Grbalpha',
    'Grbbeta',
    'Greencube',
    'Grizu263a',
    'Gt1',
    'Hadesd',
    'Inspiresat1',
    'Io86',
    'Irazu',
    'Irvine',
    'Iss',
    'Kafasat1',
    'Kashiwa',
    'Kosen1',
    'Ksu',
    'Ledsat',
    'Lightsail2',
    'Lucky7',
    'Meznsat',
    'Minxss',
    'Mitee1',
    'Mirsat1',
    'Mxl',
    'Mysat',
    'Netsat',
    'Neudose',
    'Neutron1',
    'No44',
    'Nutsat1',
    'Opssat1',
    'Oresat0',
    'Oresat05',
    'Origamisat1',
    'Painani',
    'Pegasus',
    'Picsat',
    'Planetum1',
    'Polyitan1',
    'Pwsat2',
    'Qarman',
    'Qbee',
    'Qube',
    'Qubik',
    'Quetzal1',
    'Ramsat',
    'Randev',
    'Rhoksat',
    'Roseycubesat1',
    'Sakura',
    'Salsat',
    'Sanosat1',
    'Selfiesat',
    'Sharjahsat1',
    'Siriussat',
    'Skcube',
    'Snet',
    'Spoc',
    'Sputnixusp',
    'Sr0',
    'Strand',
    'Stratosattk1',
    'Suchai2',
    'Targit',
    'Us6',
    'Uwe4',
    'Veronika',
    'Vzlusat2',
    'Yomogi',
]

FIELD_REGEX = re.compile(
    r':field (?P<field>[\*\w]+): (?P<attribute>.*?)'
    r'(?:(?=:field)|\Z|\n)', re.S)

UNKNOWN_SIZE_NOTATION = '___'


def get_attribute(obj, name):
    """
    Get element by index in case of list
    Get attribute of object by namein case of non-list object
    """
    if isinstance(obj, list):
        try:
            return obj[int(name)]
        except ValueError:
            return getattr(obj, name).name
    if isinstance(getattr(obj, name), enum.Enum):
        return getattr(obj, name).name
    return getattr(obj, name)


def get_dynamic_fields(obj, path_list, indexes, inframe_index, key):
    """
    Get element by recusion in case of unknown sized list
    """
    if inframe_index == len(path_list):
        pos = 1
        for k in indexes:
            key = key.replace(UNKNOWN_SIZE_NOTATION,
                              '_' + str(indexes[k][0] - 1) + '_', pos)
            pos += 1

        return obj, key

    name = path_list[inframe_index]
    if isinstance(obj, list):
        try:
            if name == UNKNOWN_SIZE_NOTATION:
                index_key = indexes[path_list[inframe_index - 1]][0]
                indexes[path_list[inframe_index - 1]][0] += 1
                if indexes[path_list[inframe_index - 1]][1] is None:
                    indexes[path_list[inframe_index - 1]][1] = len(obj)
                return get_dynamic_fields(obj[index_key], path_list, indexes,
                                          inframe_index + 1, key)

            return get_dynamic_fields(obj[int(name)], path_list, indexes,
                                      inframe_index + 1, key)
        except ValueError:
            return get_dynamic_fields(
                getattr(obj, name).name, path_list, indexes, inframe_index + 1,
                key)
    if isinstance(getattr(obj, name), enum.Enum):
        return get_dynamic_fields(
            getattr(obj, name).name, path_list, indexes, inframe_index + 1,
            key)
    return get_dynamic_fields(getattr(obj, name), path_list, indexes,
                              inframe_index + 1, key)


def get_fields(struct, empty=False):
    """
    Get fields defined in docstring
    """
    fields = {}
    dynamic_fields = {}

    try:
        doc_fields = FIELD_REGEX.findall(struct.__doc__)
    except TypeError:
        return fields

    for key, value in doc_fields:
        try:
            if UNKNOWN_SIZE_NOTATION not in key:
                fields[key] = functools.reduce(get_attribute, value.split('.'),
                                               struct)
            else:
                key_values = key.split(UNKNOWN_SIZE_NOTATION)
                for i in range(0, len(key_values) - 1):
                    dynamic_fields[key_values[i]] = [0, None]

                path_list = value.split('.')
                while True:
                    value, generated_key = get_dynamic_fields(
                        struct, path_list, dynamic_fields, 0, key)
                    fields[generated_key] = value
                    first_dynamic_field_key = next(iter(dynamic_fields))
                    if dynamic_fields[first_dynamic_field_key][
                            0] == dynamic_fields[first_dynamic_field_key][1]:
                        break

        except AttributeError:
            if empty:
                fields[key] = None

    return fields
