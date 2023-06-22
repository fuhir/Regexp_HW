import re
import csv
from pprint import pprint


def fields_substitution(csv_file):
    with open(csv_file, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts = list(rows)
        phonebook_contacts = []
        for contact in contacts:
            contact_str = ", ".join(contact)
            name_pattern = r"(^\w+)[,]?\s(\w+)[,]?"
            name_subs = r"\1, \2,"
            substitution1 = re.sub(name_pattern, name_subs, contact_str)
            phone_pattern = r"(\+7|8)[\s]?[\(]?([\d]{3})[\)]?[\s|\-]?([\d]{3})[\-]?([\d]{2})" \
                            r"[\-]?([\d]{2})[\s]?[\(]?([доб.]*)[\s]?([\d+]*)[\)]?"
            phone_subs = r"+7(\2)\3-\4-\5 \6\7"
            substitution2 = re.sub(phone_pattern, phone_subs, substitution1)
            len_result = len(re.findall(",", substitution2))
            if len_result > 6:
                result = substitution2.replace(" ,", "", len_result - 6)
                result = result.split(",")
                phonebook_contacts.append(result)
            else:
                substitution1 = substitution1.split(",")
                phonebook_contacts.append(substitution1)
        return phonebook_contacts


def duplicates_merging(contacts) -> list:
    mentions = []
    for count, contact_1 in enumerate(contacts):
        counter = 0
        for contact_2 in contacts:
            if contact_1[0] == contact_2[0] and contact_1[1] == contact_2[1]:
                counter += 1
                if counter > 1:
                    double_list = contacts.pop(count)
                    mentions.append(double_list)
    for contact in contacts:
        for mention in mentions:
            if contact[0] == mention[0]:
                for el, field in enumerate(contact):
                    if field == ' ':
                        contact.remove(field)
                        contact.insert(el, mention[el])
    return contacts


def write_to_csv(contacts) -> list:
    for contact in contacts:
        for count, element in enumerate(contact):
            contact[count] = element.strip()
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts)
        return contacts


if __name__ == '__main__':
    edited_contact_list = duplicates_merging(fields_substitution('phonebook_raw.csv'))
    contacts_to_csv = write_to_csv(edited_contact_list)
    pprint(contacts_to_csv)
