from core.controller import Controller

class UserInterface:
    def __init__(self, controller: Controller):
        self.__controller = controller

    def run(self):
        while True:
            print("=== Naive Bayes Classifier ===")
            print("1. Train model")
            print("2. Classify full test file")
            print("3. Classify a single record")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.__controller.train_model()

            elif choice == "2":
                self.__controller.run_file_classification()

            elif choice == "3":
                print("Enter values for the record:")
                # Example input loop (assumes same order as dataset)
                record = {}
                fields = ['UsingIP', 'LongURL', 'ShortURL', 'Symbol@', 'Redirecting//', 'PrefixSuffix-', 'SubDomains',
                          'HTTPS', 'DomainRegLen', 'Favicon', 'NonStdPort', 'HTTPSDomainURL', 'RequestURL', 'AnchorURL',
                          'LinksInScriptTags', 'ServerFormHandler', 'InfoEmail', 'AbnormalURL', 'WebsiteForwarding',
                          'StatusBarCust', 'DisableRightClick', 'UsingPopupWindow', 'IframeRedirection', 'AgeofDomain',
                          'DNSRecording', 'WebsiteTraffic', 'PageRank', 'GoogleIndex', 'LinksPointingToPage',
                          'StatsReport']

                for field in fields:
                    value = input(f"  {field}: ")
                    try:
                        record[field] = int(value)
                    except ValueError:
                        print(f"[WARNING] Invalid input for {field}, defaulting to 0.")
                        record[field] = 0

                self.__controller.run_single_classification(record)

            elif choice == "4":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.\n")