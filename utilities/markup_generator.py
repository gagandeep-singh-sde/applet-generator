from utilities.syllabic_convertor import SyllabicConvertor

syllabic_convertor = SyllabicConvertor()


def highlight_mph(mph):
    if "=" not in mph:
        return mph
    parts = mph.split("=")
    form = ""
    pcount = len(parts)
    if pcount == 2:
        form = '<span class="bold">{}</span>{}'.format(parts[0], parts[1])
    else:
        n = -1
        while len(parts):
            part = parts.pop()
            if n >= pcount:
                break
            n += 1
            if n == 0 and pcount > 1:
                fclass = ""
                form = "<span class='bold {}'>{}</span>".format(fclass, part)
            elif n == 1 and pcount == 4:
                form = "<span class='italic'>{}</span>{}".format(part, form)
            elif n > 1 and pcount != 4:
                form = "<span class='bold'>{}</span>{}".format(part, form)
            elif n == (pcount - 1) and pcount == 4:
                form = "<span class='bold'>{}</span>{}".format(part, form)
            else:
                form = "{}{}".format(part, form)
    return form


def export_cell(entries, is_syllabic):
    if len(entries) < 1:
        return "<td></td>"
    if len(entries) == 1 and "fm" in entries[0]:
        if is_syllabic:
            return "<td title=\"{}\" class='syllabics'>{}</td>".format(
                entries[0]["gl"][0],
                syllabic_convertor.to_syllabics(entries[0]["fm"][0]),
            )
        return '<td title="{}">{}</td>'.format(
            entries[0]["gl"][0],
            highlight_mph(entries[0]["mph"][0]),
        )
    line = ""
    for entry in entries:
        if "fm" not in entry or len(entry["fm"]) < 1:
            line = "{}<tr><td></td></tr>".format(line)
        elif is_syllabic:
            line = "{}<tr><td class='syllabics' title=\"{}\">{}</td></tr>".format(
                line, entry["gl"][0], syllabic_convertor.to_syllabics(entry["fm"][0])
            )
        else:
            line = '{}<tr><td title="{}">{}</td></tr>'.format(
                line, entry["gl"][0], highlight_mph(entry["mph"][0])
            )
    return "<td><table>{}</table></td>".format(line)


def export_prn(output, prn, row, isSyllabic):
    prn_titles = {
        "0": "châkwân",
        "0p": "châkwâna",
        "0'": "châkwâyuw",
        "0'p": "châkwâyuwa",
        "1": "nîy",
        "2": "chîy",
        "3": "wîy",
        "4": "aniyâyuwa (ut-awâsima)",
        "1p": "nîyân",
        "21p": "chîyânuw",
        "2p": "chîyiwâw",
        "3p": "wîyiwâw",
        "4p": "aniyâyuwa (ut-awâsima)",
        "X": "châkwân",
        "Xp": "châkwâna",
        "X'": "châkwâyuw",
        "X'p": "châkwâyuwa",
        "X→0": "châkwân",
        "X→0'": "châkwâyuw",
        "X→0p": "châkwâna",
        "X→0'p": "châkwâyuwa",
        "1→2": "nîy→chîy",
        "2→1": "chîy→nîy",
        "1→2p": "nîy→chîyiwâw",
        "2p→1": "chîyiwâw→nîy",
        "1p→2": "nîyân→chîy",
        "2→1p": "chîy→nîyân",
        "1p→2p": "nîyân→chîyiwâw",
        "2p→1p": "chîyiwâw→nîyân",
        "1→3": "nîy→ wîy",
        "3→1": "wîy→ nîy",
        "3p→1": "wîyiwâw→nîy",
        "1→3p": "nîy→ wîyiwâw",
        "4→1": "wîy (ut-awâsima)→ nîy",
        "1→4": "nîy→ wîy (ut-awâsima)",
        "3→2": "wîy→ chîy",
        "2→3": "chîy→ wîy",
        "3p→2": "wîyiwâw→ chîy",
        "2→3p": "chîy→ wîyiwâw",
        "2→4": "chîy→ aniyâyuwa (ut-awâsima)",
        "4→2": "aniyâyuwa (ut-awâsima)→ chîy",
        "1p→3": "nîyân→wîy",
        "3→1p": "wîy→nîyân",
        "3p→1p": "wîyiwâw→nîyân",
        "1p→3p": "nîyân→wîyiwâw",
        "4→1p": "aniyâyuwa (ut-awâsima)→nîyân",
        "1p→4": "nîyân→ aniyâyuwa (ut-awâsima)",
        "3→21p": "wîy→chîyânuw",
        "21p→3": "chîyânuw→wîy",
        "3p→21p": "wîyiwâw→chîyânuw",
        "21p→3p": "chîyânuw→ wîyiwâw",
        "21p→4": "chîyânuw→ aniyâyuwa (ut-awâsima)",
        "4→21p": "aniyâyuwa (ut-awâsima)→ chîyânuw",
        "3→2p": "wîy→ chîyiwâw",
        "2p→3": "chîyiwâw→ wîy",
        "3p→2p": "wîyiwâw→ chîyiwâw",
        "2p→3p": "chîyiwâw→ wîyiwâw",
        "2p→4": "chîyiwâw→ aniyâyuwa (ut-awâsima)",
        "4→2p": "aniyâyuwa (ut-awâsima)→ chîyiwâw",
        "4→3": "aniyâyuwa (ut-awâsima)→ wîy",
        "3→4": "wîy→ aniyâyuwa (ut-awâsima)",
        "4→3p": "aniyâyuwa (ut-awâsima)→ wîyiwâw",
        "3p→4": "wîyiwâw → aniyâyuwa (ut-awâsima)",
        "5→3": "niyâyuwa (ut-awâsimiyuwa)→ wîy",
        "3→5": "wîy→ niyâyuwa (ut-awâsimiyuwa)",
        "5→3p": "wîy (ut-awâsimiyuwa)→ wîyiwâw",
        "3p→5": "wîyiwâw→ wîy (ut-awâsimiyuwa)",
        "4→5": "aniyâyuwa (utawâsima)→ niyâyuwa (ut-awâsimiyuwa)",
        "5→4": "wîy (utawâsimiyuwa)→ wîy (ut-awâsima)",
        "X→1": "awân→ nîy",
        "X→2": "awân→ chîy",
        "X→1p": "awân→ nîyân",
        "X→21p": "awân→ chîyânuw",
        "X→2p": "awân→ chîyiwâw",
        "X→3": "awân→ wîy",
        "X→3p": "awân→ wîyiwâw",
        "X→4": "awân→ aniyâyuwa (ut-awâsima)",
    }
    prn_title = ""
    if prn in prn_titles:
        prn_title = prn_titles[prn]
        if isSyllabic:
            prn_title = syllabic_convertor.to_syllabics(prn_title)
    if isinstance(row, dict) and prn in row and isinstance(row[prn], list):
        dialects = ""

        for e in row[prn]:
            if "dl" in e:
                dialects = '{}<tr><td style="text-align:right; ">{}</td></tr>'.format(
                    dialects, e["dl"][0]
                )
        dialects = '<table class="multi">{}</table>'.format(dialects)
        return '{}<td style="text-align:right; "><!--dialect-->{}</td><td><!-- sound --></td><td style="text-align:right; min-width:15px;" title="{}">{}</td> {}'.format(
            output,
            dialects,
            prn_title,
            prn.replace("-", "→"),
            export_cell(row[prn], isSyllabic),
        )
    if "fm" not in row:
        return '{}<td></td><td><!-- sound --></td><td style="text-align:right; min-width:50px;" title=""></td> <td title=""></td>'.format(
            output
        )
    if isSyllabic:
        return '{}<td></td><td><!-- sound --></td><td style="text-align:right; min-width:50px;" title="{}">{}</td> <td title="{}" class=\'syllabics\'>{}</td>'.format(
            output,
            prn_title,
            prn.replace("-", "→"),
            row["gl"][0],
            syllabic_convertor.to_syllabics(row["fm"][0]),
        )
    if "mph" not in row:
        return '{}<td></td><td><!-- sound --></td><td style="text-align:right; min-width:50px;" title="{}">{}</td> <td title="{}">{}</td>'.format(
            output,
            prn_title,
            prn.replace("-", "→"),
            row["gl"][0],
            highlight_mph(row["fm"][0]),
        )
    return '{}<td></td><td><!-- sound --></td><td style="text-align:right; min-width:50px;" title="{}">{}</td> <td title="{}">{}</td>'.format(
        output,
        prn_title,
        prn.replace("-", "→"),
        row["gl"][0],
        highlight_mph(row["mph"][0]),
    )
