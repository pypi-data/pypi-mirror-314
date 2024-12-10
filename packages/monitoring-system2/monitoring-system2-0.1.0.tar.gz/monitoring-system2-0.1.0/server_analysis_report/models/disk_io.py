# -*- coding: utf-8 -*-
import psutil
import logging
from odoo import models, fields, api
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class DiskIOPerformance(models.Model):
    _name = 'disk.io.performance'
    _description = 'Disk I/O Performance Monitoring'
    _order = 'create_date desc'

    name = fields.Char(string='Measurement Point', required=True)

    # Existing Metrics
    read_count = fields.Integer(string='Read Operations')
    write_count = fields.Integer(string='Write Operations')
    read_bytes = fields.Float(string='Read Bytes (MB)', compute='_compute_bytes')
    write_bytes = fields.Float(string='Write Bytes (MB)', compute='_compute_bytes')
    read_time = fields.Float(string='Read Time (ms)')
    write_time = fields.Float(string='Write Time (ms)')
    io_time = fields.Float(string='Total I/O Time (ms)')

    # New Throughput Metrics
    read_throughput = fields.Float(
        string='Read Throughput',
        help='Megabytes read per second',
        compute='_compute_throughput',
        store=True
    )
    write_throughput = fields.Float(
        string='Write Throughput',
        help='Megabytes written per second',
        compute='_compute_throughput',
        store=True
    )

    # Previous metrics for throughput calculation
    previous_read_bytes = fields.Float(string='Previous Read Bytes')
    previous_write_bytes = fields.Float(string='Previous Write Bytes')
    previous_timestamp = fields.Datetime(string='Previous Timestamp')
    # print("previous_timestamp",previous_timestamp)

    create_date = fields.Datetime(string='Timestamp', default=fields.Datetime.now)

    @api.depends('read_bytes', 'write_bytes')
    def _compute_bytes(self):
        """function for compute read and write bytes"""
        for record in self:
            # print("nnnnnn", psutil.disk_io_counters())
            record.read_bytes = psutil.disk_io_counters().read_bytes/ (1024 * 1024)  # Convert to MB
            record.write_bytes = psutil.disk_io_counters().write_bytes / (1024 * 1024)  # Convert to MB

    @api.model
    def collect_disk_io_performance(self):
        """
        Collect Disk I/O Performance Metrics
        """
        try:
            # Get the last recorded performance record
            last_record = self.search([], order='create_date desc', limit=1)
            print("last_record",last_record)

            # Get disk I/O statistics
            disk_io = psutil.disk_io_counters()

            # Prepare performance record data
            performance_data = {
                'name': f'Disk I/O Measurement - {datetime.now()}',
                'read_count': disk_io.read_count,
                'write_count': disk_io.write_count,
                'read_bytes': disk_io.read_bytes,
                'write_bytes': disk_io.write_bytes,
                'read_time': disk_io.read_time,
                'write_time': disk_io.write_time,
                'io_time': disk_io.busy_time,
            }

            # Add previous metrics if available
            if last_record:
                print("yes")
                performance_data.update({
                    'previous_read_bytes': last_record.read_bytes * (1024 * 1024),  # Convert back to bytes
                    'previous_write_bytes': last_record.write_bytes * (1024 * 1024),  # Convert back to bytes
                    'previous_timestamp': last_record.create_date,
                })

            # Create a new performance record
            performance_rec = self.create(performance_data)

            _logger.info(f'Disk I/O Performance collected: {performance_rec.name}')

            # Cleanup old records (keep last 30 days)
            self._cleanup_old_records()

            return performance_rec

        except Exception as e:
            _logger.error(f'Error collecting Disk I/O Performance: {str(e)}')
            return False


    @api.depends('read_bytes', 'write_bytes', 'previous_read_bytes', 'previous_write_bytes', 'create_date',
                 'previous_timestamp')
    def _compute_throughput(self):
        """function for computing throughput"""
        for record in self:
            # Calculate time difference in seconds
            print("self",self)
            print("record.read_bytes",record.read_bytes)
            print("record",record.create_date)
            if record.previous_timestamp and record.create_date:
                time_diff = (record.create_date - record.previous_timestamp).total_seconds()
                print("time_diff", time_diff)

                # Prevent division by zero
                if time_diff > 0:
                    # Calculate throughput (MB/s)
                    read_throughput = (record.previous_read_bytes - record.read_bytes ) / time_diff
                    record.read_throughput = read_throughput/(1024 ** 2)
                    write_throughput = (record.previous_write_bytes- record.write_bytes) / time_diff
                    record.write_throughput = write_throughput / (1024 ** 2)
                else:
                    record.read_throughput = 0
                    record.write_throughput = 0
            else:
                record.read_throughput = 0
                record.write_throughput = 0

    def _cleanup_old_records(self):
        """
        Delete performance records older than 30 days
        """
        thirty_days_ago = datetime.now() - timedelta(days=30)
        old_records = self.search([('create_date', '<', thirty_days_ago)])
        old_records.unlink()

    def action_view_disk_io_performance(self):
        """
        Action to view disk I/O performance records
        """
        return {
            'name': 'Disk I/O Performance',
            'type': 'ir.actions.act_window',
            'res_model': 'disk.io.performance',
            'view_mode': 'tree,form',
            'context': {},
        }
