import json
import requests
import svgwrite
from PIL import Image
import io
import json
def take_inputs():
    global file_name
    global auth_option
    global option
    global base_url
    global header_params
    global query_params
    global table_name
    global doc_url
    global endpoint
    global extract_path
    global primary_key
    global auth_url
    global token_url
    global refresh_url




    file_name = input("Enter file name: ")

    print("Options:")
    print("1. http-basic")
    print("2. http-bearer")
    print("3. apikey-auth-header")
    print("4. apikey-custom-header")
    print("5. oauth2/refresh-token-with-client-credentials ")
    print("6. oauth2/authorization-code-flow")
    print("7. oauth2/default")
    print("8. oauth2/authorization-code-with-client-credentials")
    print("9. oauth2/password-grant-with-client-credentials")
    auth_option = input("Enter the option number: ")

    base_url = input("Enter base URL: ")

    header_params = input("Enter header params: ")
    header_params = header_params.split()
    header_params = [f'"{param}"' for param in header_params]
    header_params = ' '.join(header_params)

    query_params = input("Enter query params: ")
    query_params = query_params.split()
    query_params = [f'"{param}"' for param in query_params]
    query_params = ' '.join(query_params)

    table_name = input("Enter table name: ")
    doc_url = input("Enter doc URL: ")
    endpoint = input("Enter endpoint: ")
    extract_path = input("Enter extract path: ")
    primary_key = input("Enter primary key: ")
    auth_url = input("Enter auth URL: ")
    token_url = input("Enter token URL: ")
    refresh_url = input("Enter refresh URL: ")

try:
    file_location = input("Enter the file location: ")

    with open(file_location, 'r') as file:
        json_data = json.load(file)

        file_name = json_data["file_name"]
        option = json_data["Option"]
        base_url = json_data["base_url"]

        header_params = json_data["header_params"]
        header_params = header_params.split()
        header_params = [f'"{param}"' for param in header_params]
        header_params = ' '.join(header_params)

        query_params = json_data["query_params"]
        query_params = query_params.split()
        query_params = [f'"{param}"' for param in query_params]
        query_params = ' '.join(query_params)

        table_name = json_data["table_name"]
        doc_url = json_data["doc_url"]
        endpoint = json_data["endpoint"]
        extract_path = json_data["extract_path"]
        primary_key = json_data["primary_key"]
        auth_url = json_data["auth_url"]
        token_url = json_data["token_url"]
        refresh_url = json_data["refresh_url"]

        if not any([file_name, option, base_url, header_params, query_params,
                    table_name, doc_url, endpoint, extract_path, primary_key,
                    auth_url, token_url, refresh_url]):
            print("Json is empty")
            take_inputs()



except FileNotFoundError:
    take_inputs()



def generate_clj_file():


    if option == "1":
        content = f'''(config
    (password-field
      :name        "privateKey"
      :label       "Private key"
      :placeholder "Enter the Password")

    (text-field
      :name        "publicKey"
      :label       "Public Key"
      :placeholder "Enter the username"))'''
    elif option == "2":
        content = f'''(config
    (Text-field
      :name        "bearer_token"
      :label       "bearer token"
      :placeholder "Enter the bearer token"))'''
    elif option == "3":
        content = f'''(config
  (password-field
    :name        "apiKey"
    :label       "Enter API key"
    :placeholder "API key goes here"
    :required    true))'''
    elif option == "4":
        content = f'''(config
    (password-field
        :name        "apiKey"
        :label       "API key"
        :placeholder "Enter API key"
        :required    true
    )
)'''
    elif option == "5":
        content = f'''(config
    (text-field
        :name "clientId"    ;name is fixed
        :label "Enter clientId"
        :placeholder "Enter client id"
        :required    true
        (api-config-field))

    (text-field
        :name "clientSecret"    ;name is fixed
        :label "Enter clientSecret"
        :placeholder "Enter client secret"
        :required    true
        (api-config-field :masked true))

    (oauth2/refresh-token-with-client-credentials
        :api-auth-fields "refreshToken accessToken" 
                          ; we should not specify "clientAccess" here 
                          ; as clientId and clientSecret are annotated above
        (access-token
            (source
                (http/post
                    :url "{token_url}"
                    (body-params
                        "response_type" "code"
                        "client_id" "{{clientId}}"
                        "client_secret" "{{clientSecret}}"
                        "scope" "contact_read all_contact_read"
                    )
                )
            )
            (fields ;; field's names are fixed
                access-token :<= "access_token"
                refresh-token :<= "refresh_token"
                token-type :<= "token_type"
                scope :<= "scope"
                realm-id :<= "realmId"
                expires-in :<= "expires_in"
            )
        )

        (refresh-token
            (source
                (http/get
                    :url "{refresh_url}"
                    (query-params
                        "response_type" "code"
                        "client_id" "{{clientId}}"
                        "refresh_token" "$REFRESH-TOKEN"
                        "scope" "contact_read all_contact_read"
                    )
                )
            )
            (fields ;; field's names are fixed
                refresh-token :<=  "refresh_token"
                access-token  :<= "access-token"
            )
        )
    )
)'''
    elif option == "6":
        content = f'''(config
    (oauth2/authorization-code-flow
        :credential-type "DRIFT_OAUTH"
        :api-auth-fields "clientAccess refreshToken accessToken"
        (authorization-code
            (source
                (http/get
                    :base-url ""
                    :url "{auth_url}"
                    (query-params
                        "response_type" "code"
                        "client_id" "$CLIENT-ID"
                        "redirect_uri" "$FIVETRAN-APP-URL/integrations/drift/oauth2/return" ;;return-path
                        "scope" "contact_read all_contact_read"
                    )
                )
            )
        )

        (access-token
            (source
                (http/post
                     :base-url ""
                     :url "{token_url}"
                     (body-param-format "application/x-www-form-urlencoded")
                     (body-params
                          "code" "$AUTHORISATION-CODE"
                          "client_id" "$CLIENT-ID"
                          "client_secret" "$CLIENT-SECRET"
                          "grant_type" "authorization_code"
                      )
                 )
            )
            (fields ;; field's names are fixed
                access-token :<= "access_token"
                refresh-token :<= "refresh_token"
                token-type :<= "token_type"
                scope :<= "scope"
                realm-id :<= "realm-id"
                expires-at :<= "expires_at"
            )
        )

        (refresh-token
            (source
                (http/post
                     :base-url ""
                     :url "{refresh_url}"
                     (body-param-format "application/x-www-form-urlencoded")
                     (body-params
                          "code" "$AUTHORISATION-CODE"
                          "client_id" "$CLIENT-ID"
                          "client_secret" "$CLIENT-SECRET"
                          "grant_type" "authorization_code"
                      )
                 )
            )
            (fields ;; field's names are fixed
                refresh-token :<=  "refresh_token"
                access-token  :<= "access-token"
            )
        )
    )
)'''
    elif option == "7":
        content = f'''(config
  (text-field
      :name        "subDomain"
      :label       "Company Name"
      :placeholder "fivetran"
      :required    true
      (api-config-field))
  (oauth2/default (oauth2-constants
                :credential-type "XYZ_OAUTH"
                :api-auth-fields "clientAccess" ;adds clientId and clientSecret fields
                :response-type  "code"
                :scope             nil
                :access-type       nil
                :prompt            nil
                :authorization-uri  "{auth_url}"
                :return-path  "/integrations/namely/oauth2/return"
                :token-uri  "{token_url}"
                :grant-type "refresh_token"
                :state "get_token"
                  )))'''
    elif option == "8":
        content = f'''(config
 (text-field
  :name "clientId"
  :label "Enter Client Id"
  :placeholder "Client Id goes here"
  :required    true
  (api-config-field))

 (text-field
  :name "clientSecret"
  :label "Enter Client Secret"
  :placeholder "Client Secret goes here"
  :required    true
  (api-config-field :masked true))

 (oauth2/authorization-code-with-client-credentials
  :api-auth-fields "refreshToken accessToken" 
                     ; we should not specify "clientAccess" here 
                     ; as clientId and clientSecret are annotated above
  (authorization-code
   (source
    (http/get
     :base-url ""
     :url  "{auth_url}"
     (query-params
      "response_type" "code"
      "client_id" "{{clientId}}"
      "scope" "contact_read all_contact_read conversation_read user_read account_read playbook_read"
      "redirect_uri" "$FIVETRAN-APP-URL/integrations/drift/oauth2/return" ;;return-path
      )
     )
    )
   )

  (access-token
   (source
    (http/post
     :base-url ""
     :url "{token_url}"
     (body-param-format "application/x-www-form-urlencoded")
     (body-params
      "code" "$AUTHORISATION-CODE"
      "client_id" "{{clientId}}"
      "client_secret" "{{clientSecret}}"
      "grant_type" "authorization_code"
      )
     )
    )

   (fields ;; field's names are fixed
    access-token :<= "access_token"
    refresh-token :<= "refresh_token"
    token-type :<= "token_type"
    scope :<= "scope"
    realm-id :<= "realm-id"
    expires-at :<= "expires_at"
    )
   )

  (refresh-token
   (source
    (http/post
     :base-url ""
     :url "{refresh_url}"
     (query-params
      "refresh_token" "$REFRESH-TOKEN"
      "client_id" "{{clientId}}"
      "client_secret" "{{clientSecret}}"
      "grant_type" "refresh_token"
      )
     )
    )
   (fields
    refresh-token :<=  "refresh_token"
    access-token  :<= "access_token"
    )
   )
  )
 )'''
    elif option == "9":
        content = f'''(text-field
    :name        "clientSecret" ; name is fixed
    :label       "Enter clientSecret"
    :placeholder ""
    :required    true
    (api-config-field :masked true))

  (text-field
    :name        "username" ; name is fixed
    :label       "Enter username"
    :placeholder ""
    :required    true
    (api-config-field))

  (text-field
    :name        "password" ; name is fixed
    :label       "Enter password"
    :placeholder ""
    :required    true
    (api-config-field :masked true))

  (oauth2/password-grant-with-client-credentials
    (access-token
      (source
        (http/post
          :base-url "{auth_url}"
          :url      "/oauth2/token"
          (body-param-format "application/json")
          (body-params
            "grant_type" "password"
            "client_id" "{{clientId}}"
            "client_secret" "{{clientSecret}}"
            "username" "{{username}}"
            "password" "{{password}}"
            "scope" "contact_read all_contact_read")))

      (fields ; field's names are fixed
        access-token :<= "access_token"
        refresh-token :<= "refresh_token"
        token-type :<= "token_type"
        scope :<= "scope"
        realm-id :<= "realm-id"
        expires-at :<= "expires_at"))

    (refresh-token
      (source
        (http/post
          :base-url "{refresh_url}"
          :url      "/oauth2/token"
          (body-params
            "grant_type" "refresh_token"
            "client_id" "{{clientId}}"
            "client_secret" "{{clientSecret}}"
            "username" "{{username}}"
            "refresh_token" "$REFRESH-TOKEN")))
      (fields
        refresh-token :<= "refresh_token"
        access-token :<= "access_token"))))'''
    else:
        print("Invalid option selected.")
        return

    content += f'''

(default-source
  (http/get :base-url "{base_url}"
    (header-params {header_params}))
  (paging/no-pagination)
  (auth/{'http-basic' if option == "1" else ('http-bearer' if option == "2" else ('apikey-auth-header' if option == "3" else('apikey-custom-header' if option == "4" 
                                                                                                                             else('oauth2/refresh-token-with-client-credential' if option == "4" else('oauth2/default')))))})
  (error-handler
    (when :status 429 :action rate-limit)))

(temp-entity {table_name}
  (api-docs-url "{doc_url}")
  (source
    (http/get :url "{endpoint}")
    (extract-path "{extract_path}")
    (setup-test
      (upon-receiving :code 200 (pass))))
  (fields
    id         :id     :<="{primary_key}"))'''

    with open(f"{file_name}.clj", "w") as file:
        file.write(content)

    print(f"{file_name}.clj file generated successfully!")
def take_inputs():
    global name
    global description
    global url
    global service
    global capture_deletes

    name = input("Enter API name: ")
    mdname = name.replace(' ', '-')
    oname = name.replace(' ', '_')
    description = input("Enter API description: ")
    url = input("Enter API URL: ")
    print("Choose the type:")
    print("1. Marketing")
    print("2. HumanResources")
    print("3. Finance")
    print("4. Productivity")
    print("5. Engineering")
    print("6. Support")
    print("7. Sales")
    print("8. Security")
    print("9. BITool")
    service = int(input("Enter the choice number: "))
    capture_deletes = input("Enter the capture_delete leave empty if null")
try:
    file_location = "input.json"

    with open(file_location, 'r') as file:
        json_data = json.load(file)

        name = json_data["name"]
        mdname = name.replace(' ', '-')
        oname = name.replace(' ', '_')
        description= json_data["description"]
        url = json_data["url"]
        capture_deletes = json_data["capture_deletes"]

        service = json_data["service"]


        if not any([name, description, url, service]):
            take_inputs()

except FileNotFoundError:
    take_inputs()

def generate_setup_guide(mdname, oname):
    setup_guide = (
        f"# {cap(name)} Setup Guide {{{{ typeBadge \"{oname.lower()}\" }}}} {{{{ availabilityBadge \"{oname.lower()}\" }}}}\n"
        f"\n"
        f"Follow our setup guide to connect {cap(name)} to Fivetran.\n"
        f"\n"
        f"------\n"
        f"\n"
        f"## Prerequisites\n"
        f"\n"
        f"To connect {cap(name)} to Fivetran, you need a [{cap(name)}]({url}) account.\n"
        f"\n"
        f"------\n"
        f"\n"
        f"## Setup instructions\n"
        f"\n"
        f"### <span class=\"step-item\">Heading</span>\n"
        f"Write Steps here\n"
        f"> Note : \n"
        f"\n"
        f"### <span class=\"step-item\">Finish Fivetran configuration </span>\n"
        f"\n"
        f"Steps here\n"
        f"\n"
        f"-----\n"
        f"\n"
        f"## Related articles\n"
        f"\n"
        f"[<i aria-hidden=\"true\" class=\"material-icons\">description</i> Connector Overview](/docs/applications/{mdname})\n"
        f"\n"
        f"<b> </b>\n"
        f"\n"
        f"[<i aria-hidden=\"true\" class=\"material-icons\">home</i> Documentation Home](/docs/getting-started)\n"
    )
    with open(f"{mdname.lower()}-setup-guide.md", "w") as f:
        f.write(setup_guide)

def cap(sentence):
    words = sentence.split()
    capitalized_words = [word.capitalize() for word in words]
    capitalized_sentence = ' '.join(capitalized_words)
    return capitalized_sentence


def ico_to_svg(ico_data):
    # Open ICO data
    ico_image = Image.open(ico_data)

    # Get the size of the ICO image
    width, height = ico_image.size

    # Create a new SVG drawing
    dwg = svgwrite.Drawing()

    # Set the size of the SVG canvas
    dwg['width'] = f"{width}px"
    dwg['height'] = f"{height}px"

    # Iterate over each pixel in the ICO image and set the corresponding SVG pixel
    for y in range(height):
        for x in range(width):
            pixel = ico_image.getpixel((x, y))
            dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill=f"rgb{pixel[:3]}"))

    # Return the SVG code
    return dwg.tostring()


def generate_files(name, description, url, mdname, oname):
    name_md = (
        f"# {cap(name)} {{{{ typeBadge \"{oname.lower()}\" }}}} {{{{ availabilityBadge \"{oname.lower()}\" }}}}\n"
        f"\n"
        f"[{cap(name)}]({url}) {description}\n\n"
        f"-----\n"
        f"\n"
        f"## Features\n"
        f"\n"
        f"{{{{#featureTable \"{oname.lower()}\"}}}}\n"
        f"Capture Deletes: {capture_deletes}\n"
        f"Column Hashing:\n"
        f"Data Blocking: \n"
        f"Re-sync:\n"
        "{{/featureTable}}\n"
        f"\n"
        f"-----\n"
        f"\n\n"
        f"## Setup guide\n"
        f"\n"
        f"Follow our [step-by-step {cap(name)} setup guide](/docs/applications/{mdname.lower()}/setup-guide) to connect {cap(name)} with your destination using Fivetran connectors.\n"
    )
    with open(f"{mdname.lower()}.md", "w") as f:
        f.write(name_md)

    type_mapping = {
        1: "Marketing",
        2: "HumanResources",
        3: "Finance",
        4: "Productivity",
        5: "Engineering",
        6: "Support",
        7: "Sales",
        8: "Security",
        9: "BITool"
    }

    ss = type_mapping.get(service, "")
    name_config_yaml = f"""---
service:
  name: "{cap(name)}"
  description: "{description}"
  docsPath: "/docs/applications/{mdname.lower()}"
  logo: "/integrations/coil_connectors/resources/{oname.lower()}/resources/{oname.lower()}.svg"
  availability: "development"
  connectorType: "lite"
  coil:
    type: "{ss}"
    languageVersion: "2.0.0"
api: {{}}
metrics: {{}}
"""
    with open(f"{oname.lower()}.config.yaml", "w") as f:
        f.write(name_config_yaml)

    name_yaml = f"""    - name: {cap(name)}
      hidden: true
      file: {mdname.lower()}.md
      path: /docs/applications/{mdname.lower()}
      title: {cap(name)} connector by Fivetran | Fivetran documentation
      description: Connect your {cap(name)} data to your destination using Fivetran. Learn about configuration requirements, setup, and ERDs with our technical documentation.
      children:
        - name: Setup Guide
          hidden: true
          file: {mdname.lower()}-setup-guide.md
          path: /docs/applications/{mdname.lower()}/setup-guide
          title: {cap(name)} data connector by Fivetran | Setup Guide
          description: Read step-by-step instructions on how to connect {cap(name)} with your destination using Fivetran connectors."""
    with open(f"{oname.lower()}.yaml", "w") as f:
        f.write(name_yaml)

    response = requests.get(url)
    html_content = response.text

    favicon_url = None
    link_tags = html_content.split('<link ')
    for link_tag in link_tags:
        if 'rel="shortcut icon"' in link_tag or 'rel="icon"' in link_tag or 'rel="apple-touch-icon"' in link_tag:
            href_index = link_tag.find('href=')
            if href_index != -1:
                url_start = link_tag.find('"', href_index)
                url_end = link_tag.find('"', url_start + 1)
                favicon_url = link_tag[url_start + 1:url_end]
                break

    if favicon_url:
        if not favicon_url.startswith('http'):
            favicon_url = url.rstrip('/') + favicon_url


        link_tags = html_content.split('<link ')
        response = requests.get(favicon_url)
        favicon_data = response.content

        # Check if the favicon is in ICO format
        if response.headers.get('content-type') == 'image/x-icon':
            # Convert ICO to SVG
            svg_code = ico_to_svg(io.BytesIO(favicon_data))

            # Save the SVG code to a file
            with open(f"{oname.lower()}.svg", "w") as file:
                file.write(svg_code)

            print(f"SVG code saved as {name.lower()}.svg")
        elif response.headers.get('content-type') == 'image/svg+xml':
            with open(f"{oname.lower()}.svg", "wb") as file:
                file.write(favicon_data)
                print(f"SVG favicon saved as {oname.lower()}.svg")
        else:
            try:
                # Check if the favicon is in PNG format
                favicon_image = Image.open(io.BytesIO(favicon_data))
                # Convert PNG to ICO
                ico_data = io.BytesIO()
                favicon_image.save(ico_data, format='ICO')
                ico_data.seek(0)

                # Convert ICO to SVG
                svg_code = ico_to_svg(ico_data)

                # Save the SVG code to a file
                with open(f"{oname.lower()}.svg", "w") as file:
                    file.write(svg_code)

                print(f"SVG code saved as {name.lower()}.svg")
            except:
                print("Favicon is neither in ICO nor PNG format.")
    else:
        print("No favicon found.")



generate_setup_guide(mdname, oname)
generate_files(name, description, url, mdname, oname)
generate_clj_file()



