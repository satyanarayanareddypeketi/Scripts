
require 'fileutils'
require 'yaml'
yml_file = YAML.load_file('config.yml')
count=0
result=File.exist?("TEST-TestEnvTestCases.txt")
if result==true
        file_handler = File.open("TEST-TestEnvTestCases.txt")
        for line in file_handler do
                count=count+1
                if count==2
                        temp = line.split(" ")
                        total_tests = temp[2].chop
                        failed_tests = temp[4].chop
                end
        end
else
        raise "Build Failed"
end
puts total_tests
puts failed_tests
FileUtils.rm_rf("TEST-TestEnvTestCases.txt")
if failed_tests == 0
        puts "Code will Deploy to PreProd Environment"
else
        puts failed_tests.to_f/total_tests.to_f
        if ((failed_tests.to_f/total_tests.to_f)*100).to_i <= (100-yml_file["PreProdEnv"]["percentage"])
                puts "Code will Deploy to PreProd Environment"
        else
                raise  "Code will not Deploy to PreProd Environment"
        end
end
