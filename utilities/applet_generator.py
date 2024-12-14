import codecs
from utilities.syllabic_convertor import SyllabicConvertor
from utilities.markup_generator import export_prn

syllabicConvertor = SyllabicConvertor()


def GenerateApplet(entries):
    output = '<h1 text-align="center">Naskapi Verbs Conjugation</h1> \r\n\t<div class="tab"><ul class="tabnav"> <!-- Verb Classes -->\r\n\tVerb Classes:'
    database = {}
    mxKey = "mx4"
    prns = {
        "0": "1",
        "0p": "2",
        "0'": "3",
        "0'p": "4",
        "1": "04",
        "2": "01",
        "3": "06",
        "4": "08",
        "1p": "05",
        "21p": "03",
        "2p": "02",
        "3p": "07",
        "4p": "09 ",
        "X": "10",
        "Xp": "11",
        "X'": "12",
        "X'p": "13",
        "X→0": "10",
        "X→0'": "11",
        "X→0p": "12",
        "X→0'p": "13",
        "1→2": "01",
        "2→1": "01",
        "1→2p": "02",
        "2p→1": "02",
        "1p→2": "03a",
        "2→1p": "03a",
        "1p→2p": "03b",
        "2p→1p": "03b",
        "1→3": "04",
        "3→1": "04",
        "3p→1": "05",
        "1→3p": "05",
        "4→1": "06",
        "1→4": "06",
        "3→2": "07",
        "2→3": "07",
        "3p→2": "08",
        "2→3p": "08",
        "2→4": "09",
        "4→2": "09",
        "1p→3": "10",
        "3→1p": "10",
        "3p→1p": "11",
        "1p→3p": "11",
        "4→1p": "12",
        "1p→4": "12",
        "3→21p": "13",
        "21p→3": "13",
        "3p→21p": "14",
        "21p→3p": "14",
        "21p→4": "15",
        "4→21p": "15",
        "3→2p": "16",
        "2p→3": "16",
        "3p→2p": "17",
        "2p→3p": "17",
        "2p→4": "18",
        "4→2p": "18",
        "4→3": "19",
        "3→4": "19",
        "4→3p": "20",
        "3p→4": "20",
        "5→3": "21",
        "3→5": "21",
        "5→3p": "22",
        "3p→5": "22",
        "4→5": "23",
        "5→4": "23",
        "X→1": "25",
        "X→2": "24",
        "X→1p": "28",
        "X→21p": "27",
        "X→2p": "26",
        "X→3": "29",
        "X→3p": "30",
        "X→4": "31",
    }
    for entry in entries:
        # sort database
        if "ps" not in entry:
            continue
        ps = entry["ps"][0]
        if ps not in database:
            database[ps] = {}
        if "pdm1" not in entry:
            continue
        pdm = entry["pdm1"][0]
        if pdm not in database[ps]:
            database[ps][pdm] = {}
        if "stm" not in entry:
            continue
        stm = entry["stm"][0]
        if stm not in database[ps][pdm]:
            database[ps][pdm][stm] = {}
        if "wn" not in entry:
            continue
        wn = entry["wn"][0]
        if wn not in database[ps][pdm][stm]:
            database[ps][pdm][stm][wn] = {}
        if mxKey in entry:
            mx = entry[mxKey][0]
        if "prn" not in entry:
            continue
        prn = entry["prn"][0]
        if prn.replace("-0", "") in prns:
            mx = prns[prn.replace("-0", "")]
        grp = hd = dir = "-"
        if "hd1" in entry:
            hd = entry["hd1"][0]
        if "dir" in entry:
            dir = entry["dir"][0]
        grp = dir
        if "un" in hd:
            grp = hd
            hd = dir = "-"
        elif " " in hd or ps in "vta":
            grp = hd
            if " " in grp:
                grp = grp[0 : grp.index(" ")]
            # if ps in "vta": hd = dir
        if grp not in database[ps][pdm][stm][wn]:
            database[ps][pdm][stm][wn][grp] = {}
        if mx not in database[ps][pdm][stm][wn][grp]:
            database[ps][pdm][stm][wn][grp][mx] = {}

        if ps in "vti vai+o vta":
            if hd not in database[ps][pdm][stm][wn][grp][mx]:
                database[ps][pdm][stm][wn][grp][mx][hd] = {}
            if prn not in database[ps][pdm][stm][wn][grp][mx][hd]:
                database[ps][pdm][stm][wn][grp][mx][hd][prn] = []
            database[ps][pdm][stm][wn][grp][mx][hd][prn].append(entry)
        else:
            if prn not in database[ps][pdm][stm][wn][grp][mx]:
                database[ps][pdm][stm][wn][grp][mx][prn] = []
            database[ps][pdm][stm][wn][grp][mx][prn].append(entry)

    pss = sorted(database.keys())
    for ps in pss:
        output = (
            "%s\r\n\t<li class=' %s' id='%s' title=''><a href='#' class='%s' name='%s' onclick='selectAllTabs(this); return false;'>%s</a></li>"
            % (output, ps, ps, ps, ps, ps)
        )
    output = "%s</ul>" % output

    # end of sorting
    # begin formating
    for ps in database.keys():
        output = (
            '%s\r\n\t<div  id="c_%s" class="hidden"><div class="tab"><ul class="tabnav">\ Conjugations:\ '
            % (output, ps)
        )
        pdms = sorted(database[ps])
        print(ps, ": ", pdms)
        if pdms is None:
            continue

        for pdm in pdms:
            className = "in"
            if pdm in "11a 11b 12a 12b 13a 13b 14a 14b 15 16":
                className = "co"
            if "17" in pdm:
                className = "im"
            output = (
                "%s\r\n\t\t<li class='%s' id='_%s_%s' title=''><a href='#' class=' %s' name='%s' onclick='selectAllTabs(this); return false;'>%s</a></li>"
                % (output, pdm, ps, pdm, className, pdm, pdm)
            )
        output = "%s</ul>" % output

        for pdm in pdms:
            output = (
                '%s\r\n\t\t<div  id="c__%s_%s" class="hidden"> <div class="tab"><ul class="tabnav">\ Stems:'
                % (output, ps, pdm)
            )
            stms = sorted(database[ps][pdm])

            for stm in stms:
                output = (
                    "%s\r\n\t\t\t<li class='%s' id='_%s_%s_%s' title=''><a href='#' class=' %s' name='%s' onclick='selectAllTabs(this); return false;'>%s</a></li>"
                    % (output, stm, ps, pdm, stm.replace(" ", "_"), stm, stm, stm)
                )
            output = "%s</ul>" % output

            for stm in stms:
                output = (
                    '%s\r\n\t\t\t<div  id="c__%s_%s_%s" class="hidden"><div class="tab"><ul class="tabnav"> '
                    % (output, ps, pdm, stm.replace(" ", "_"))
                )

                verbs = sorted(database[ps][pdm][stm])
                for wn in verbs:
                    output = (
                        "%s\r\n\t\t\t\t<li class='%s syllabics' id='_%s_%s_%s_%s' title=''><a href='#' class=' %s syllabics' name='%s' onclick='selectAllTabs(this); return false;'>%s</a></li>"
                        % (
                            output,
                            syllabicConvertor.to_syllabics(wn),
                            ps,
                            pdm,
                            stm.replace(" ", "_"),
                            syllabicConvertor.to_syllabics(wn).replace(" ", "_"),
                            syllabicConvertor.to_syllabics(wn),
                            syllabicConvertor.to_syllabics(wn),
                            syllabicConvertor.to_syllabics(wn),
                        )
                    )

                    output = (
                        "%s\r\n\t\t\t\t<li class='%s' id='_%s_%s_%s_%s' title=''><a href='#' class=' %s' name='%s' onclick='selectAllTabs(this); return false;'>%s</a></li>"
                        % (
                            output,
                            wn,
                            ps,
                            pdm,
                            stm.replace(" ", "_"),
                            wn.replace(" ", "_"),
                            wn,
                            wn,
                            wn,
                        )
                    )

                output = "%s</ul>" % output
                for wn in database[ps][pdm][stm]:
                    tables = ["syllabics", "roman"]
                    print(ps, pdm, stm, wn)
                    for table in tables:
                        wnD = wn
                        if "syl" in table:
                            wnD = syllabicConvertor.to_syllabics(wn)
                        output = (
                            '%s\r\n\t\t\t<div  id="c__%s_%s_%s_%s" class="hidden"><table  class="info %s" style=" margin:2em;"> '
                            % (
                                output,
                                ps,
                                pdm,
                                stm.replace(" ", "_"),
                                wnD.replace(" ", "_"),
                                ps,
                            )
                        )
                        grps = sorted(database[ps][pdm][stm][wn])

                        if ps in "vti vai+o":
                            output = (
                                "%s\r\n\t\t\t<thead><tr><th colspan='5'></th><td class='spacer'></td><th colspan='5'>Relational</th></tr><tbody>"
                                % output
                            )

                            for grp in grps:
                                mxs = sorted(database[ps][pdm][stm][wn][grp])
                                for i, mx in enumerate(mxs):
                                    rowClass = ""
                                    if (i % 2) == 0:
                                        rowClass = "alt"
                                    if i == 0:
                                        output = (
                                            '%s\r\n\t\t\t\t\t<tr class="%s"  style="border-top: 3px solid #dda601"><th  class="%s" rowspan="%d" style="  border-right: 1px solid #ffffce; min-width: 150px; text-align: center">%s</th>'
                                            % (
                                                output,
                                                rowClass,
                                                rowClass,
                                                len(mxs),
                                                grp.replace("-", ""),
                                            )
                                        )
                                    else:
                                        output = '%s\r\n\t\t\t\t\t<tr class="%s">' % (
                                            output,
                                            rowClass,
                                        )

                                    if "-" in database[ps][pdm][stm][wn][grp][mx]:
                                        row = database[ps][pdm][stm][wn][grp][mx]["-"]
                                        prn = list(row.keys())[0]
                                        output = (
                                            '%s<td class="spacer">&nbsp;</td>'
                                            % export_prn(
                                                output, prn, row, "syl" in table
                                            )
                                        )
                                    if (
                                        "relational"
                                        in database[ps][pdm][stm][wn][grp][mx]
                                    ):
                                        row = database[ps][pdm][stm][wn][grp][mx][
                                            "relational"
                                        ]
                                        prn = list(row.keys())[0]
                                        output = export_prn(
                                            output, prn, row, "syl" in table
                                        )
                                    if "unspecified actor" in grp:
                                        output = (
                                            " %s<td></td><td></td><td></td><td></td>"
                                            % output
                                        )
                                    output = "%s</tr>" % output

                        elif ps in "vta":
                            output = (
                                "%s<tbody><tr><td style=\"padding:0; margin:0; border-right: 3px solid #dda601\"> <table class='passive'><thead><tr><th></th><th colspan='5'>Direct</th><th colspan='5'>Inverse</th></tr></thead><tbody>"
                                % output
                            )
                            passives = ""
                            lastHD = ""
                            for grp in grps:
                                mxs = sorted(database[ps][pdm][stm][wn][grp])
                                prevPrn = False
                                for i, mx in enumerate(mxs):
                                    rowClass = ""
                                    if (i % 2) == 0:
                                        rowClass = "alt"

                                    if "passive" in database[ps][pdm][stm][wn][grp][mx]:
                                        passives = '%s\r\n\t\t\t\t\t<tr class="%s">' % (
                                            passives,
                                            rowClass,
                                        )
                                        row = database[ps][pdm][stm][wn][grp][mx][
                                            "passive"
                                        ]
                                        prn = list(row.keys())[0]
                                        passives = "%s</tr>" % export_prn(
                                            passives, prn, row, "syl" in table
                                        )
                                    else:
                                        if (
                                            grp in "mixed direct"
                                            and "mixed direct"
                                            in database[ps][pdm][stm][wn][grp][mx]
                                        ):
                                            if prevPrn == False:
                                                prevPrn = list(
                                                    database[ps][pdm][stm][wn][grp][mx][
                                                        "mixed direct"
                                                    ].keys()
                                                )[0][0:2]
                                            elif (
                                                list(
                                                    database[ps][pdm][stm][wn][grp][mx][
                                                        "mixed direct"
                                                    ].keys()
                                                )[0][0:2]
                                                not in prevPrn
                                            ):
                                                rowClass = (
                                                    '%s" style="border-top: 2px solid #dda601"'
                                                    % rowClass
                                                )
                                                prevPrn = list(
                                                    database[ps][pdm][stm][wn][grp][mx][
                                                        "mixed direct"
                                                    ].keys()
                                                )[0][0:2]
                                        if i == 0:
                                            output = (
                                                '%s\r\n\t\t\t\t\t<tr class="%s"  style="border-top: 3px solid #dda601"><th class="%s" rowspan="%d" style="  border-right: 1px solid #ffffce; min-width: 150px; text-align: center">%s</th>'
                                                % (
                                                    output,
                                                    rowClass,
                                                    rowClass,
                                                    len(mxs),
                                                    grp,
                                                )
                                            )
                                        else:
                                            output = (
                                                '%s\r\n\t\t\t\t\t<tr class="%s">'
                                                % (
                                                    output,
                                                    rowClass,
                                                )
                                            )
                                        dirs = sorted(
                                            database[ps][pdm][stm][wn][grp][mx].keys()
                                        )

                                        print(wn, grp, dirs)
                                        for dir in dirs:
                                            row = database[ps][pdm][stm][wn][grp][mx][
                                                dir
                                            ]
                                            prn = list(row.keys())[0]
                                            output = export_prn(
                                                output, prn, row, "syl" in table
                                            )

                                        output = "%s</tr>" % output

                            passives = (
                                '<tr><th colspan="6">Passive</th></tr>%s' % passives
                            )
                            output = (
                                "%s</tbody></table></td><td style='border-width:0; margin:0;  vertical-align:top; background:white; padding:0 2rem;'><table class='passive'><tbody>%s</tbody></table></td></tr>"
                                % (output, passives)
                            )
                        else:
                            output = "%s\r\n\t\t\t<tbody>" % output
                            for grp in grps:
                                mxs = sorted(database[ps][pdm][stm][wn][grp])
                                for i, mx in enumerate(mxs):
                                    rowClass = ""
                                    if (i % 2) == 1:
                                        rowClass = "alt"
                                    output = '%s\r\n\t\t\t\t\t<tr class="%s">' % (
                                        output,
                                        rowClass,
                                    )
                                    for prn in database[ps][pdm][stm][wn][grp][mx]:
                                        for entry in database[ps][pdm][stm][wn][grp][
                                            mx
                                        ][prn]:
                                            output = export_prn(
                                                output, prn, entry, "syl" in table
                                            )
                                    output = "%s</tr>" % output

                        output = "%s</tbody></table></div>" % output
                output = "%s</div></div>" % output
            output = "%s</div></div>" % output
        output = "%s</div></div>" % output
    output = "%s</div></div>" % output

    # endof formating

    # read template file
    reader = codecs.open(filename="utilities/template.html", encoding="utf-8")
    html = reader.readlines()
    reader.close()
    # import output into template

    # write file
    writer = codecs.open(filename="applet.html", mode="w", encoding="utf-8")
    writer.write(
        "".join(html).replace(
            "</body>",
            "%s</body>" % (output),
        )
    )
    writer.close()

    return "applet.html"
