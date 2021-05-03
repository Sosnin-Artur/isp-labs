import argparse
import configparser

from serializers.src.serializer_creator import serializer_creator

from os import path

def get_paths():
    parser = argparse.ArgumentParser(description = 'Serializer')
    group = parser.add_mutually_exclusive_group(required = True)

    group.add_argument('-j', '--json',
                       nargs = '+', type = str,
                       help = "json serialization")
    group.add_argument('-t', '--toml',
                       nargs = '+', type = str,
                       help = "toml serialization")
    group.add_argument('-p', '--pickle',
                       nargs = '+', type = str,
                       help = "pickle serialization")    
    group.add_argument('-y', '--yaml',
                       nargs = '+', type = str,
                       help = "yaml serialization")
    
    args  =  vars(parser.parse_args())
    format_, file_  =  tuple(*{arg: value for arg, value
                             in args.items() if value}.items())
    if format_ == 'config':
        config = configparser.ConfigParser()
        config.read(file_[0])
        return config['FORMAT']['serializer'], [config['FILE']['name']]
    else:
        return format_, file_

def main():    
    format_, files = get_paths()    
    factory = serializer_creator.Creator()

    out_ser = factory.create_deserializer(format_)    
    obj = out_ser.load(files[0])
        
    extension = path.splitext(files[1])[1]    
    in_ser = factory.create_serializer(extension[1:])
    in_ser.dump(obj, files[1])    

if __name__ == "__main__":
    main()
    