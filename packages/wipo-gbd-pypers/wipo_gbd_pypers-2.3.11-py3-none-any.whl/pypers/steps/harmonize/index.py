import os
import subprocess
from pypers.core.interfaces.storage.backup import Backup
from pypers.core.interfaces import db
from pypers.utils.utils import clean_folder, delete_files
from pypers.steps.base.step_generic import EmptyStep
from pypers.utils.package_explorer import write_masks_to_json
from pypers.core.interfaces.config.pypers_storage import GBD_DOCUMENTS, IDX_BUCKET, IMAGES_BUCKET
class Index(EmptyStep):
    """
    Index / Backup / DyDb publish
    """
    spec = {
        "version": "2.0",
        "descr": [
            "Returns the directory with the extraction"
        ],
        "args":
        {
            'inputs': [
                {
                    'name': 'idx_files',
                    'descr': 'files to be indexed',
                },
                {
                    'name': 'extraction_dir',
                    'descr': 'files to be indexed',
                },

            ],
            'outputs': [
                {
                    'name': 'flag',
                    'descr': 'flag for done'
                }
            ],
            "params": [
                {
                    "name": "uat",
                    "type": "int",
                    "descr": "an int flag (0|1) whether to "
                             "chain uat to the next pipeline",
                    "value": 0
                }
            ]
        }
    }

    # "files" : {
    #     "st13" : {
    #         "idx" : "000/st13/idx.json",
    #         "latest" : "000/st13/latest.json"
    #     },
    #     ...
    # }
    def process(self):
        region = os.environ.get('AWS_DEFAULT_REGION', 'eu-central-1')
        if not len(self.idx_files):
            return
        self.collection_name = self.collection.replace('_harmonize', '')
        self.backup = Backup(self.output_dir, self.pipeline_type, self.collection_name)

        st13s = {}
        # rewrite paths to absolute paths
        # Make sure to get st13 here and after upload to s3/ local disc + dyndb.
        for archive in self.idx_files:
            st13s.update({os.path.basename(os.path.dirname(record['gbd'])): {
                'gbd':record['gbd'],
                'dyn_live': record['dyn_live']}
            for record in archive})
        live_documents = []
        for st13 in st13s.keys():
            gbd_file = st13s[st13]['gbd']
            local_path = self.backup.store_doc_gbd(gbd_file, st13, hard=True)
            st13s[st13]['local_gbd'] = local_path
            live_documents.append(st13s[st13]['dyn_live'])
        self.backup.run_upload_command()

        db.get_pre_prod_db().put_items(live_documents)

        # index the files
        failed_log = os.path.join(self.output_dir, 'failed.index')
        jar_file = os.environ.get('INDEXER_JAR').strip()

        # write fofn file
        fofn_file = os.path.join(self.output_dir, 'findex.fofn')
        fofn_file_dynamo = os.path.join(self.output_dir, 'findex.dyn')
        masks_file = os.path.join(self.output_dir, 'masks.json')
        aws_extra_config = os.path.join(self.output_dir, 'config_aws.yml')
        payload_aws_extra = """
batchSize: 1000
threads: 0
bucket_gbd: %s
bucket_img: %s
bucket_idx: %s
type2shards:
%s
        """
        payload_aws_extra_args = {
            'designs': """
  designs:
    - designxa
    - designxb
    - designxc
    - designxd
    - designxe
    - designxf
    - designxg""",
            'brands': """
  brands:
    - brandxa
    - brandxb
    - brandxc
    - brandxd
    - brandxe
    - brandxf
    - brandxg"""
        }
        with open(aws_extra_config, 'w') as f:
            f.write(payload_aws_extra % (GBD_DOCUMENTS, IMAGES_BUCKET, IDX_BUCKET, payload_aws_extra_args[self.pipeline_type]))
        with open(fofn_file, 'w') as f, open(fofn_file_dynamo, 'w') as g:
            for st13 in st13s.keys():
                x = st13s[st13]
                f.write('%s\n' % x['local_gbd'])
                g.write('%s\n' % x['dyn_live'])

        write_masks_to_json(masks_file)

        suffix = '' if self.pipeline_type == 'brands' else '_GDD'
        solr = os.environ.get('SLRW_URL%s' % suffix)
        template = os.environ.get('TEMPLATE_URL%s' % suffix)
        config = os.environ.get('INDEXER_CONF_URL%s' % suffix)
        cmd = 'java -Daws.region=%s -jar %s --paths %s --logFile %s --collection %s --type %s --patch %s --mode transform_batch --nums file://%s --awsConf file://%s --solr %s --template %s --config %s'
        p_type = self.pipeline_type
        if int(self.uat):
            p_type = 'uat'
        cmd = cmd % (region,
                     jar_file,
                     fofn_file,
                     failed_log,
                     self.collection_name,
                     p_type,
                     self.pipeline_type[:-1],
                     masks_file,
                     aws_extra_config,
                     solr,
                     template,
                     config
                     )

        proc = subprocess.Popen(cmd.split(' '),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                close_fds=True)
        stdout, stderr = proc.communicate()

        rc = proc.returncode
        if rc != 0:
            print(str(stdout))
            db.get_db_error().send_error(self.run_id,
                                         self.collection_name,
                                         {'source': 'indexer'},
                                         "%s" % str(stderr))
            raise Exception("Indexer error")

        if os.path.exists(failed_log):
            with open(failed_log, 'r') as f:
                for line in f.readlines():
                    st13 = os.path.basename(os.path.dirname(line))
                    self.logger.info("Failed indexing on %s" % st13)
                    st13s.pop(st13)

        #self._del_files(st13s)
        for folder in self.extraction_dir:
            clean_folder(folder)

    def postprocess(self):
        failed_log = os.path.join(self.output_dir, 'failed.index')
        if os.path.exists(failed_log):
            os.remove(failed_log)
        self.flag = [1]

    def _del_files(self, st13s):
        for st13, path in st13s.items():
            os.remove(path)