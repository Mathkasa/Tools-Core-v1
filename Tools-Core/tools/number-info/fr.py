import phonenumbers
from phonenumbers import geocoder, carrier, timezone as ph_timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

NUMBER_TYPES = {
    phonenumbers.PhoneNumberType.MOBILE:          "Mobile",
    phonenumbers.PhoneNumberType.FIXED_LINE:      "Fixe",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou Mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE:       "NumÃ©ro gratuit",
    phonenumbers.PhoneNumberType.PREMIUM_RATE:    "SurtaxÃ©",
    phonenumbers.PhoneNumberType.SHARED_COST:     "CoÃ»t partagÃ©",
    phonenumbers.PhoneNumberType.VOIP:            "VoIP",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personnel",
    phonenumbers.PhoneNumberType.PAGER:           "Pager",
    phonenumbers.PhoneNumberType.UAN:             "UAN",
    phonenumbers.PhoneNumberType.UNKNOWN:         "Inconnu",
}


def analyser_numero(phone_number):
    try:
        parsed = phonenumbers.parse(phone_number, None)
    except phonenumbers.NumberParseException as e:
        return None, f"Impossible d'analyser le numÃ©ro : {e}"

    if not phonenumbers.is_valid_number(parsed):
        return None, "NumÃ©ro invalide"

    indicatif = f"+{parsed.country_code}"
    operateur = carrier.name_for_number(parsed, "fr") or "Inconnu"
    type_num = NUMBER_TYPES.get(phonenumbers.number_type(parsed), "Inconnu")
    fuseaux = ph_timezone.time_zones_for_number(parsed)
    fuseau = fuseaux[0] if fuseaux else "Inconnu"
    pays = phonenumbers.region_code_for_number(parsed) or "Inconnu"
    region = geocoder.description_for_number(parsed, "fr") or "Inconnu"
    formate_national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    formate_international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    possible = phonenumbers.is_possible_number(parsed)

    infos = {
        "NumÃ©ro saisi":         phone_number,
        "Format national":      formate_national,
        "Format international": formate_international,
        "Statut":               "[bold green]Valide[/bold green]",
        "Possible":             "[bold green]Oui[/bold green]" if possible else "[bold red]Non[/bold red]",
        "Indicatif pays":       indicatif,
        "Pays":                 pays,
        "RÃ©gion":               region,
        "Fuseau horaire":       fuseau,
        "OpÃ©rateur":            operateur,
        "Type de numÃ©ro":       type_num,
    }
    return infos, None


def afficher(infos):
    table = Table(
        title="[bold red]Informations NumÃ©ro de TÃ©lÃ©phone[/bold red]",
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold red",
        show_lines=True,
    )
    table.add_column("Champ", style="bold white", width=22)
    table.add_column("Valeur", style="cyan")

    for champ, valeur in infos.items():
        table.add_row(champ, str(valeur))

    console.print()
    console.print(table)
    console.print()


if __name__ == "__main__":
    try:
        console.print()
        console.print(Panel(
            "[bold red]TOOLS-CORE[/bold red] â€” [bold white]Number Info[/bold white]",
            border_style="red",
            box=box.DOUBLE_EDGE,
        ))
        console.print()

        numero = console.input(
            "[bold red][[/bold red][bold white]=[/bold white][bold red]][/bold red] "
            "NumÃ©ro de tÃ©lÃ©phone (avec indicatif, ex: +33612345678) : "
        ).strip()

        if not numero:
            console.print("[bold red][!] NumÃ©ro vide. AnnulÃ©.[/bold red]")
            raise SystemExit(0)

        infos, erreur = analyser_numero(numero)

        if erreur:
            console.print(f"[bold red][!] {erreur}[/bold red]")
        else:
            afficher(infos)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red][!] Interrompu.[/bold red]")


