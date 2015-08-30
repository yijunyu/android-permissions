for directory in */; do
    echo $directory
    cp compare-all-versions.py $directory/compare-all-versions.py
    cp compare.py $directory/compare.py
    cd $directory
    echo "comparing permissions across all versions"
    python compare-all-versions.py --manifest manifestpermissions.xml --code code_permissions_2.2.3.xml code_permissions_2.3.6.xml code_permissions_3.2.2.xml code_permissions_4.0.1.xml code_permissions_4.1.1.xml --output comparison_all.xml
    for code in `ls code_permissions*`; do
        echo "comparison for version ${code:17:5}"
        python compare.py manifestpermissions.xml $code comparison_${code:17:5}.xml
    done
    rm compare-all-versions.py
    rm compare.py
    cd ..
done
