#!/usr/bin/python
# vim:fileencoding=utf-8:sw=4:et

# Copyright (c) 2013 Mike FABIAN <mfabian@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os
from lxml import etree

import langtable
from langtable import list_locales
from langtable import list_keyboards

opts = {}
opts['debug'] = False

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='lang-table')
    parser.add_argument('-T', '--territoriesfilename',
                        nargs='?',
                        type=str,
                        default='./territories.xml',
                        help='territories file, default is ./territories.xml')
    parser.add_argument('-K', '--keyboardsfilename',
                        nargs='?',
                        type=str,
                        default='./keyboards.xml',
                        help='keyboards file, default is ./keyboards.xml')
    parser.add_argument('-L', '--languagesfilename',
                        nargs='?',
                        type=str,
                        default='./languages.xml',
                        help='languages file, default is ./languages.xml')
    parser.add_argument('-l', '--logfilename',
                        nargs='?',
                        type=str,
                        default='./langtable.log',
                        help='log file, default is ./langtable.log')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='print debugging output')
    return parser.parse_args()

translations_languages = {}
translations_territories = {}

def read_translations_from_cldr_file(file = None):
    translations_languages.clear()
    translations_territories.clear()
    if file:
        ldmlTree = etree.parse(file).getroot()
        if ldmlTree.tag != 'ldml':
            print "error: Wrong ldmlTree.tag=%(tag)s." %ldmlTree.tag
            exit(1)
        if len(ldmlTree):
            for element in ldmlTree:
                if element.tag == 'localeDisplayNames':
                    localeDisplayNamesTree = element
                    if len(localeDisplayNamesTree):
                        for element in localeDisplayNamesTree:
                            if element.tag == 'languages':
                                languagesTree = element
                                if len(languagesTree):
                                    for element in languagesTree:
                                        languageId = element.get('type')
                                        translation = element.text
                                        if not (element.get('alt') == 'short' and languageId in translations_languages):
                                            translations_languages[languageId] = translation
                            if element.tag == 'territories':
                                territoriesTree = element
                                if len(territoriesTree):
                                    for element in territoriesTree:
                                        territoryId = element.get('type')
                                        translation = element.text
                                        if not (element.get('alt') == 'short' and territoryId in translations_territories):
                                            translations_territories[territoryId] = translation
    return

def get_translations_from_cldr(main_cldr_dir = None):
    for target_language in sorted(langtable.languages):
        cldr_file = main_cldr_dir+'/'+target_language+'.xml'
        if not os.path.exists(cldr_file):
            continue
        read_translations_from_cldr_file(cldr_file)
        for language_to_translate in translations_languages:
            if language_to_translate in langtable.languages:
                if target_language not in langtable.languages[language_to_translate].names:
                    print "Missing: %(language_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'language_to_translate': language_to_translate,
                          'target_language': target_language,
                          'tr': translations_languages[language_to_translate].encode('UTF-8')}
                    langtable.languages[language_to_translate].names[target_language] = translations_languages[language_to_translate]
                elif translations_languages[language_to_translate] \
                     == langtable.languages[language_to_translate].names[target_language]:
                    if opts['debug']:
                        print "Identical: %(language_to_translate)s → %(target_language)s = %(tr)s" \
                            %{'language_to_translate': language_to_translate,
                              'target_language': target_language,
                              'tr': translations_languages[language_to_translate].encode('UTF-8')}
                else:
                    print "- %(language_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'language_to_translate': language_to_translate,
                          'target_language': target_language,
                          'tr': langtable.languages[language_to_translate].names[target_language].encode('UTF-8')}
                    print "+ %(language_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'language_to_translate': language_to_translate,
                          'target_language': target_language,
                          'tr': translations_languages[language_to_translate].encode('UTF-8')}
            else:
                if opts['debug']:
                    print "Not in lang-table: %(language_to_translate)s" \
                        %{'language_to_translate': language_to_translate}
        for territory_to_translate in translations_territories:
            if territory_to_translate in langtable.territories:
                if target_language not in langtable.territories[territory_to_translate].names:
                    print "Missing: %(territory_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'territory_to_translate': territory_to_translate,
                          'target_language': target_language,
                          'tr': translations_territories[territory_to_translate].encode('UTF-8')}
                    langtable.territories[territory_to_translate].names[target_language] = translations_territories[territory_to_translate]
                elif translations_territories[territory_to_translate] \
                     == langtable.territories[territory_to_translate].names[target_language]:
                    if opts['debug']:
                        print "Identical: %(territory_to_translate)s → %(target_language)s = %(tr)s" \
                            %{'territory_to_translate': territory_to_translate,
                              'target_language': target_language,
                              'tr': translations_territories[territory_to_translate].encode('UTF-8')}
                else:
                    print "- %(territory_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'territory_to_translate': territory_to_translate,
                          'target_language': target_language,
                          'tr': langtable.territories[territory_to_translate].names[target_language].encode('UTF-8')}
                    print "+ %(territory_to_translate)s → %(target_language)s = %(tr)s" \
                        %{'territory_to_translate': territory_to_translate,
                          'target_language': target_language,
                          'tr': translations_territories[territory_to_translate].encode('UTF-8')}
            else:
                if opts['debug']:
                    print "Not in lang-table: %(territory_to_translate)s" \
                        %{'territory_to_translate': territory_to_translate}
    return

def main():
    args = parse_args()
    if args.debug:
        opts['debug'] = True
    else:
        opts['debug'] = False

    langtable.init(debug = True,
                    logfilename = args.logfilename,
                    territoriesfilename = args.territoriesfilename,
                    languagesfilename = args.languagesfilename,
                    keyboardsfilename = args.keyboardsfilename)

    get_translations_from_cldr(main_cldr_dir='/local/mfabian/src/cldr-svn/trunk/common/main')

    langtable.write_files(territoriesfilename = args.territoriesfilename+'.new',
                           languagesfilename = args.languagesfilename+'.new',
                           keyboardsfilename = args.keyboardsfilename+'.new')


if __name__ == '__main__':
    main()
