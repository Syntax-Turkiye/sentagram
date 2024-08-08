import json
from data_preprocessing import revise_start_end


class SentagramDataAugmentation:
    def __init__(self, file_path):
        self.file_path = file_path

    def augment(self, type1, type2):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        augmented_data = []
        for sentence in data['sentences']:
            is_type1_exist = False
            is_type2_exist = False
            for element in sentence['elements']:
                if type1 == element["type"]:
                    is_type1_exist = True
                if type2 == element["type"]:
                    is_type2_exist = True
            if is_type1_exist and is_type2_exist:
                new_elements = sentence["elements"].copy()

                type1_index = next(i for i, item in enumerate(new_elements) if item["type"] == type1)
                type2_index = next(i for i, item in enumerate(new_elements) if item["type"] == type2)

                new_elements[type1_index], new_elements[type2_index] = new_elements[type2_index], new_elements[
                    type1_index]

                words = [elem["word"] for elem in new_elements]
                new_text = " ".join(words) + "."

                new_data = {
                    "id": sentence["id"],
                    "text": new_text,
                    "elements": new_elements
                }
                print(new_data)
                augmented_data.append(new_data)
        data['sentences'].extend(augmented_data)
        with open(f"aug_{self.file_path}", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.file_path = f"aug_{self.file_path}"


if __name__ == '__main__':
    augmenter = SentagramDataAugmentation('data/1500_ham_veri.json')
    augmenter.augment("ozne", "yuklem")
    augmenter.augment("z-tum", "yuklem")
